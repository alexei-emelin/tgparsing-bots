import asyncio
from datetime import datetime
from typing import Dict

from pyrogram import Client, errors
from pyrogram.raw import types
from pyrogram.types import Chat, ChatPreview, User


async def get_chat_info(client: Client, chat: str) -> Chat | None:
    try:
        chat_info = await client.get_chat(chat)
    except errors.UsernameNotOccupied:
        return None
    if isinstance(chat_info, ChatPreview):
        return None
    return chat_info


async def get_member_info(user: User) -> tuple:
    user_info = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "phone_number": user.phone_number,
    }
    return user.id, user_info


async def get_geomember_info(user: types.User) -> tuple:
    info = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "phone_number": user.phone,
    }
    return user.id, info


async def get_chat_data(chat: types.Channel):
    info = {
        "title": chat.title,
        "username": chat.username,
    }
    return info


async def get_commenting_members(
    client: Client,
    chat: Chat,
    parsed_chat: str,
    to_date: datetime,
    from_date: datetime,
):
    history = client.get_chat_history(
        chat_id=parsed_chat,
        offset_date=to_date,
    )
    channel_users: Dict[int, dict] = {}
    if not history:
        return channel_users
    async for item in history:
        if item.date < from_date:
            break
        replies = client.get_discussion_replies(chat.id, item.id)
        if not replies:
            continue
        try:
            async for reply in replies:
                user = reply.from_user
                if not user or user.is_bot:
                    continue
                user_id, member_info = await get_member_info(user)
                if user_id not in channel_users:
                    member_info["groups"] = [f"t.me/{chat.username}"]
                    channel_users.update({user_id: member_info})
        except errors.MsgIdInvalid:
            continue
        except errors.FloodWait as exp:
            await asyncio.sleep(exp.value + 1)
    return channel_users
