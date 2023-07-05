from pyrogram import Client, errors
from pyrogram.enums import ChatType
from pyrogram.raw import types
from pyrogram.types import Chat, User


async def get_group_info(client: Client, chat: str) -> Chat | None:
    try:
        chat_info = await client.get_chat(chat)
    except errors.UsernameNotOccupied:
        return None
    if chat_info.type is not ChatType.CHANNEL:
        return None
    return chat_info


def get_member_info(user: User) -> dict:
    info = {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "phone_number": user.phone_number,
    }
    return info


def get_geomember_info(user: types.User) -> dict:
    info = {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "phone_number": user.phone,
    }
    return info


def get_chat_info(chat: types.Channel):
    info = {
        "title": chat.title,
        "username": chat.username,
    }
    return info
