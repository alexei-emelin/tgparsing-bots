import time
import typing
from datetime import datetime

from pyrogram import Client, enums
from pyrogram.errors import FloodWait, MsgIdInvalid
from pyrogram.raw import functions, types

from bot import utils as ut
from settings import config


async def members_parser(
    client: Client,
    parsed_chats: typing.List[str],
) -> typing.List[dict]:
    all_data = []
    for parsed_chat in parsed_chats:
        chat = await ut.get_group_info(client, parsed_chat)
        if not chat or chat.type not in [
            enums.ChatType.GROUP,
            enums.ChatType.SUPERGROUP,
        ]:
            continue
        members_gen = client.get_chat_members(
            chat_id=parsed_chat,
        )
        chat_members = {
            "chat": {
                "title": chat.title,
                "description": chat.description,
                "username": chat.username,
            },
            "members": [
                ut.get_member_info(member.user)
                async for member in members_gen
                if not member.user.is_bot
            ]
            if members_gen
            else [],
        }
        all_data.append(chat_members)
    return all_data


async def get_active_members_from_channel(
    client: Client,
    parsed_chats: typing.List[str],
    from_date: datetime,
    to_date: datetime,
) -> dict:
    all_users = {}
    for parsed_chat in parsed_chats:
        chat = await client.get_chat(parsed_chat)
        if chat.type != enums.ChatType.CHANNEL:
            continue
        history = client.get_chat_history(
            chat_id=parsed_chat,
            offset_date=to_date,
        )
        if not history:
            continue
        async for item in history:
            if item.date < from_date:
                break
            replies = client.get_discussion_replies(chat.id, item.id)
            if not replies:
                continue
            channel_users = {}
            try:
                async for reply in replies:
                    user = reply.from_user
                    if not user or user.is_bot:
                        continue
                    user_data = {user.id: ut.get_member_info(user)}
                    channel_users.update(user_data)
            except MsgIdInvalid:
                continue
            except FloodWait as exp:
                time.sleep(exp.value + 1)
            all_users.update(channel_users)
    return all_users


async def parser_by_geo(
    client: Client,
    latitude: float,
    longitude: float,
    accuracy_radius: int,
):
    resp_members = await client.invoke(
        functions.contacts.GetLocated(
            geo_point=types.InputGeoPoint(
                lat=latitude, long=longitude, accuracy_radius=accuracy_radius
            ),
            background=False,
            self_expires=0x7FFFFFFF,
        )
    )
    members = [
        ut.get_geomember_info(member)
        for member in resp_members.users
        if not member.bot
    ]
    return members


async def parser_search_chats(
    client: Client,
    query: str,
) -> list:
    chats_resp = await client.invoke(
        functions.contacts.Search(q=query, limit=config.SEARCH_LIMIT)
    )
    chats = [ut.get_chat_info(item) for item in chats_resp.chats]
    return chats
