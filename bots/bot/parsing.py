import datetime
import json
import os
import textwrap
import time
import typing

from pyrogram import Client, enums
from pyrogram.enums import ChatType
from pyrogram.errors.exceptions import bad_request_400, flood_420
from pyrogram.raw import functions
from pyrogram.raw.types import InputGeoPoint
from pyrogram.types import Chat

from bot.utils.log_func import logger


async def get_group_info(client: Client, chat: str) -> Chat | None:
    try:
        chat_info = await client.get_chat(chat)
        return chat_info
    except Exception as ex:
        return None


def get_user_info(user) -> dict:
    info = {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "phone_number": user.phone_number,
    }
    return info


def info_user_for_geo(user) -> dict:
    info = {}
    info["user_id"] = user.id
    info["first_name"] = user.first_name
    if user.last_name:
        info["last_name"] = user.last_name
    if user.username:
        info["username"] = user.username
    return info


def create_result_file(data: typing.Dict, chat_name: str) -> str:
    os.makedirs("files", exist_ok=True)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    file_path = f"files/{chat_name}_{timestr}.json"
    with open(file_path, "w", encoding="utf-8") as result_file:
        json.dump(data, result_file, ensure_ascii=False)
    return file_path


async def members_parser(
    client: Client,
    parsed_chats: typing.List[str],
) -> typing.List[dict]:
    all_data = []
    for parsed_chat in parsed_chats:
        chat = await get_group_info(client, parsed_chat)
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            continue
        chat_members = {
            "title": chat.title,
            "description": chat.description,
            "username": chat.username,
            "members": {
                member.user.id: get_user_info(member.user)
                async for member in client.get_chat_members(
                    chat_id=parsed_chat,
                )
                if not member.user.is_bot
            }
        }
        all_data.append(chat_members)
    return all_data


async def parser_chat_members_by_period(
    chat_name: str,
    period_from: datetime.date,
    period_to: datetime.date,
    api_id: int,
    api_hash: str,
    session_string: str,
):
    logger.info("Parser chat members by period")
    chat_members = {}
    async with Client(
        ":memory:", api_id, api_hash, session_string=session_string
    ) as client:
        members_list = []
        history_messages = [
            x
            async for x in client.get_chat_history(
                chat_id=chat_name, offset_date=period_to, limit=2000
            )
        ]
        for message in history_messages:
            if message.date < period_from:
                continue
            if message.from_user:
                members_list.append(message.from_user)

            for chat_member in members_list:
                user = chat_member
                info = get_user_info(user)
                if user.id not in chat_members:
                    info["count"] = 1
                    chat_members[user.id] = info
                else:
                    chat_members[user.id]["count"] += 1
    file_path = create_result_file(chat_members, chat_name)
    return file_path


async def start_parser_by_period(
    parsered_chats: typing.List[str],
    period_from: datetime.date,
    period_to: datetime.date,
    api_id: int,
    api_hash: str,
    session_string: str,
) -> typing.List[str]:
    file_paths_list = []
    for chat in parsered_chats:
        chat_type = await get_group_info(chat, api_id, api_hash, session_string)
        if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            file_path = await parser_chat_members_by_period(
                chat, period_from, period_to, api_id, api_hash, session_string
            )
            file_paths_list.append(file_path)
        else:
            info_text = f"""
            {chat} не является чатом, проверьте правильность ссылки, \
            либо воспользуйтесь другой услугой
            """
            answer = {"error": textwrap.dedent(info_text).strip()}
            file_path = create_result_file(answer, chat)
            file_paths_list.append(file_path)
    return file_paths_list


async def parser_private_channel(
    chat_name: str, api_id: int, api_hash: str, session_string: str, limit: int
):
    chat_members = {}
    async with Client(
        ":memory:", api_id, api_hash, session_string=session_string
    ) as client:
        history_messages = [
            x
            async for x in client.get_chat_history(
                chat_id=chat_name, limit=limit
            )
        ]
        for message in history_messages:
            try:
                discussion_replies = [
                    x
                    async for x in client.get_discussion_replies(
                        chat_name, message.id
                    )
                ]
                for comment in discussion_replies:
                    if not comment.from_user.is_bot:
                        info = get_user_info(comment.from_user)
                        if comment.from_user.id not in chat_members:
                            info["count"] = 1
                            chat_members[comment.from_user.id] = info
                        else:
                            chat_members[comment.from_user.id]["count"] += 1
            except bad_request_400.MsgIdInvalid:
                logger.error("Не удалось получить комментарии к посту")
                continue
            except flood_420.FloodWait as wait_err:
                logger.error(wait_err)
                logger.info("Wait %s", wait_err.value)
                time.sleep(wait_err.value)
    file_path = create_result_file(chat_members, chat_name)
    return file_path


async def start_parser_privat_chanels(
    parsered_chats: typing.List[str],
    api_id: int,
    api_hash: str,
    session_string: str,
    limit: int,
) -> typing.List[str]:
    file_paths_list = []
    for chat in parsered_chats:
        chat_type = await get_group_info(chat, api_id, api_hash, session_string)
        if chat_type == ChatType.CHANNEL:
            file_path = await parser_private_channel(
                chat, api_id, api_hash, session_string, limit
            )
            file_paths_list.append(file_path)
        else:
            info_text = f"""
            {chat} не является каналом, проверьте правильность ссылки, \
            либо воспользуйтесь другой услугой
            """
            result = {"error": textwrap.dedent(info_text).strip()}
            file_path = create_result_file(result, chat)
            file_paths_list.append(file_path)
    return file_paths_list


async def parser_by_geo(
    lat: float,
    lng: float,
    accuracy_radius: int,
    api_id: int,
    api_hash: str,
    session_string: str,
):
    logger.info("Start parse geo locate")

    nearby_users = {}
    async with Client(
        ":memory:", api_id, api_hash, session_string=session_string
    ) as client:
        response = await client.invoke(
            functions.contacts.GetLocated(
                geo_point=InputGeoPoint(
                    lat=lat, long=lng, accuracy_radius=accuracy_radius
                ),
                background=False,
                self_expires=0x7FFFFFFF,
            )
        )
        for nearby_user in response.users:
            user = nearby_user
            info = info_user_for_geo(user)
            if user.id not in nearby_users:
                info["count"] = 1
                nearby_users[user.id] = info
            else:
                nearby_users[user.id]["count"] += 1
    name = f"geopars_rad_{accuracy_radius}"
    return create_result_file(nearby_users, name)
