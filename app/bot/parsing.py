import asyncio
import typing
from datetime import datetime

from bot import utils as ut
from bot.schemas import LatLotSchema
from pyrogram import Client, enums
from pyrogram.raw import functions
from settings import config


async def members_parser(
    client: Client,
    parsed_chats: typing.List[str],
    groups_count: int,
) -> typing.Any:
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
    all_users: typing.Dict[int, dict] = {}
    for parsed_chat in parsed_chats:
        chat = await client.get_chat(parsed_chat)
        members = {}
        if chat.type == enums.ChatType.CHANNEL and activity.get("comments"):
            members = await ut.get_channel_active_members(
                client=client,
                chat=chat,
                from_date=from_date,
                to_date=to_date,
                comments=activity["comments"],
            )
        elif chat.type in [
            enums.ChatType.GROUP,
            enums.ChatType.SUPERGROUP,
        ] and activity.get("reposts"):
            members = await ut.get_group_active_members(
                client=client,
                chat=chat,  # type: ignore
                from_date=from_date,
                to_date=to_date,
                reposts=activity["reposts"],
            )
        if not members:
            continue
        for user_id, user_info in members.items():
            if user_id in all_users:
                all_users[user_id]["activity_count"] += user_info[
                    "activity_count"
                ]
                all_users[user_id]["groups"] += user_info["groups"]
            else:
                all_users.update({user_id: user_info})
    if activity_count > 1:
        return await ut.filter_by_activity_count(
            members=all_users,
            activity_count=activity_count,
        )
    return all_users


async def mass_get_by_geo(
    client: Client, coordinates: list[LatLotSchema], accuracy_radius: int
):
    all_members = {}
    for index, coordinate in enumerate(coordinates):
        members = await ut.parser_by_geo(
            client,
            coordinate.latitude,
            coordinate.longitude,
            accuracy_radius,
        )
        all_members.update(members)
        if all([len(coordinates) > 1, index < len(coordinates) - 1]):
            await asyncio.sleep(602)
    return all_members


async def parser_search_chats(
    client: Client,
    query: str,
) -> list:
    chats_resp = await client.invoke(
        functions.contacts.Search(q=query, limit=config.SEARCH_LIMIT)
    )
    chats = [await ut.get_chat_data(item) for item in chats_resp.chats]
    return chats
