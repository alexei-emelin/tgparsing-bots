import typing
from datetime import datetime

from pyrogram import Client, enums
from pyrogram.raw import functions, types

from bot import utils as ut
from settings import config


async def members_parser(
    client: Client,
    parsed_chats: typing.List[str],
    groups_count: int,
) -> dict:
    all_members: typing.Dict[int, dict] = {}
    for parsed_chat in parsed_chats:
        chat = await ut.get_chat_info(client, parsed_chat)
        if not chat or chat.type not in [
            enums.ChatType.GROUP,
            enums.ChatType.SUPERGROUP,
        ]:
            continue
        members_gen = client.get_chat_members(
            chat_id=parsed_chat,
        )
        if not members_gen:
            continue
        async for member in members_gen:
            if member.user.is_bot:
                continue
            user_id, member_info = await ut.get_member_info(member.user)
            if user_id in all_members:
                all_members[user_id]["groups"].append(f"t.me/{chat.username}")
                continue
            member_info["groups"] = [f"t.me/{chat.username}"]
            all_members[user_id] = member_info
    if not groups_count > 1:
        return all_members
    filter_members: typing.Dict[int, dict] = {}
    for key, value in all_members.items():
        if len(value["groups"]) >= groups_count:
            filter_members.update({key: value})
    return filter_members


async def get_active_members(
    client: Client,
    parsed_chats: typing.List[str],
    from_date: datetime,
    to_date: datetime,
    activity_count: int,
    activity: dict,
) -> dict:
    all_users = {}
    for parsed_chat in parsed_chats:
        chat = await client.get_chat(parsed_chat)
        if chat.type == enums.ChatType.CHANNEL and activity.get("comments"):
            members = await ut.get_commenting_members(
                client=client,
                chat=chat,
                parsed_chat=parsed_chat,
                from_date=from_date,
                to_date=to_date,
            )
            all_users.update(members)
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
        await ut.get_geomember_info(member)
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
    chats = [await ut.get_chat_data(item) for item in chats_resp.chats]
    return chats
