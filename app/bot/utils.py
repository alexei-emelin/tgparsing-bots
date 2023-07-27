import asyncio
from datetime import datetime
from typing import Dict

from pyrogram import Client, errors
from pyrogram.raw import functions, types
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
        "activity_count": 0,
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


async def filter_by_groups_count(
    members: dict, groups_count: int
) -> Dict[int, dict]:
    filter_members = {}
    for key, value in members.items():
        if len(value["groups"]) >= groups_count:
            filter_members.update({key: value})
    return filter_members


async def filter_by_activity_count(
    members: dict, activity_count: int
) -> Dict[int, dict]:
    filter_members = {}
    for user_id, user_info in members.items():
        if user_info["activity_count"] >= activity_count:
            filter_members.update({user_id: user_info})
    return filter_members


async def get_channel_active_members(
    client: Client,
    chat: Chat,
    to_date: datetime,
    from_date: datetime,
    comments: bool,
) -> Dict[int, dict]:
    history = client.get_chat_history(
        chat_id=chat.id,
        offset_date=to_date,
    )
    channel_users: Dict[int, dict] = {}
    if not history or not comments:
        return channel_users
    async for history_item in history:
        if history_item.date < from_date:
            break
        replies = client.get_discussion_replies(chat.id, history_item.id)
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
                    member_info["activity_count"] = 1
                    channel_users.update({user_id: member_info})
                else:
                    channel_users[user_id]["activity_count"] += 1
        except errors.MsgIdInvalid:
            continue
        except errors.FloodWait as exp:
            await asyncio.sleep(exp.value + 1)
    return channel_users


async def get_group_active_members(
    client: Client,
    chat: Chat,
    to_date: datetime,
    from_date: datetime,
    reposts: bool,
) -> Dict[int, dict]:
    history = client.get_chat_history(
        chat_id=chat.id,
        offset_date=to_date,
    )
    group_users: Dict[int, dict] = {}
    if not history or not reposts:
        return group_users
    async for history_item in history:
        if history_item.date < from_date:
            break
        forward_date = history_item.forward_date
        if not forward_date:
            continue
        try:
            user = history_item.from_user
            if not user or user.is_bot:
                continue
            user_id, member_info = await get_member_info(user)
            if user_id not in group_users:
                member_info["groups"] = [f"t.me/{chat.username}"]
                member_info["activity_count"] = 1
                group_users.update({user_id: member_info})
            else:
                group_users[user_id]["activity_count"] += 1
        except errors.MsgIdInvalid:
            continue
        except errors.FloodWait as exp:
            await asyncio.sleep(exp.value + 1)
    return group_users


async def parser_by_geo(
    client: Client,
    latitude: float,
    longitude: float,
    accuracy_radius: int,
) -> dict[int, dict]:
    resp_members = await client.invoke(
        functions.contacts.GetLocated(
            geo_point=types.InputGeoPoint(
                lat=latitude, long=longitude, accuracy_radius=accuracy_radius
            ),
            background=False,
            self_expires=0x7FFFFFFF,
        )
    )
    members = {}
    for member in resp_members.users:
        user_id, user_data = await get_geomember_info(member)
        user_data["groups"] = []
        members[user_id] = user_data
    return members
