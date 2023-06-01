import asyncio
import datetime
import json
import os
import time
import typing

from pyrogram import Client, types
from pyrogram.errors.exceptions import bad_request_400, flood_420
from pyrogram.raw import functions
from pyrogram.raw.types import InputGeoPoint

from bot.utils.log_func import logger


def info_user(user) -> dict:
    info = dict()
    if not user.is_bot:
        info["user_id"] = user.id
        info["first_name"] = user.first_name
        if user.last_name:
            info["last_name"] = user.last_name
        if user.username:
            info["username"] = user.username
        if user.phone_number:
            info["phone_number"] = user.phone_number
    return info


def info_user_for_geo(user) -> dict:
    info = dict()
    info["user_id"] = user.id
    info["first_name"] = user.first_name
    if user.last_name:
        info["last_name"] = user.last_name
    if user.username:
        info["username"] = user.username
    return info


def create_result_file(data: typing.Dict):
    os.makedirs("files", exist_ok=True)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    file_name = f"files/{timestr}.json"
    try:
        with open(file_name, "w", encoding="utf-8") as result_file:
            json.dump(data, result_file, ensure_ascii=False)
    except Exception as ex:
        logger.exception(ex)
        logger.error("Error save file")
        return None
    return file_name


async def parser_chat_members_by_subscribes(
    parsered_chats: list[str], api_id: int, api_hash: str, session_string: str
):
    logger.info("Parser chat members by subscribes")

    chat_members = dict()
    async with Client(
        ":memory:", api_id, api_hash, session_string=session_string
    ) as client:
        for chat_name in parsered_chats:
            _chat_members = [
                x async for x in client.get_chat_members(chat_name)
            ]
            try:
                for chat_member in _chat_members:
                    if isinstance(chat_member, types.ChatMember):
                        if chat_member.status == "left":
                            continue
                        user = chat_member.user
                    else:
                        user = chat_member
                    info = info_user(user)
                    if user.id not in chat_members:
                        info["count"] = 1
                        chat_members[user.id] = info
                    else:
                        chat_members[user.id]["count"] += 1
            except bad_request_400.ChatAdminRequired:
                logger.exception("you cant see this message")
                parser_private_channel(
                    parsered_chats, api_id, api_hash, session_string
                )
    result = create_result_file(chat_members)
    return result


async def parser_chat_members_by_period(
    parsered_chats: typing.List[str],
    period_from: datetime.date,
    period_to: datetime.date,
    api_id: int,
    api_hash: str,
    session_string: str,
):
    logger.info("Parser chat members by period")
    async with Client(
        ":memory:", api_id, api_hash, session_string=session_string
    ) as client:
        chat_members = dict()
        for chat_name in parsered_chats:
            _chat_members = []
            _period_from = datetime.datetime.fromisoformat(
                period_from.isoformat()
            )
            _period_to = datetime.datetime.fromisoformat(period_to.isoformat())
            _period_to += datetime.timedelta(days=1)
            history_messages = [
                x
                async for x in client.get_chat_history(
                    chat_id=chat_name, offset_date=_period_to, limit=2000
                )
            ]
            for message in history_messages:
                if message.date < _period_from:
                    break
                if message.from_user:
                    _chat_members.append(message.from_user)
            try:
                for chat_member in _chat_members:
                    if isinstance(chat_member, types.ChatMember):
                        if chat_member.status == "left":
                            continue
                        user = chat_member.user
                    else:
                        user = chat_member
                    info = info_user(user)
                    if user.id not in chat_members:
                        info["count"] = 1
                        chat_members[user.id] = info
                    else:
                        chat_members[user.id]["count"] += 1
            except bad_request_400.ChatAdminRequired:
                logger.exception("you cant see this message")
                parser_private_channel(
                    parsered_chats, api_id, api_hash, session_string
                )
    result = create_result_file(chat_members)
    return result


async def parser_private_channel(
    parsered_chats: typing.List[str],
    api_id: int,
    api_hash: str,
    session_string: str,
):
    async with Client(
        ":memory:", api_id, api_hash, session_string=session_string
    ) as client:
        chat_members = dict()
        for chat_name in parsered_chats:
            # for tests use
            # history_messages = [x async for x in client.get_chat_history(chat_id=chat_name, limit=10)]
            history_messages = [
                x async for x in client.get_chat_history(chat_id=chat_name)
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
                        print(comment.from_user)
                        if not comment.from_user.is_bot:
                            info = info_user(comment.from_user)
                            if comment.from_user.id not in chat_members:
                                info["count"] = 1
                                chat_members[comment.from_user.id] = info
                            else:
                                chat_members[comment.from_user.id]["count"] += 1
                except bad_request_400.MsgIdInvalid:
                    logger.exception("Не удалось получить комментарии к посту")
                    continue
                except flood_420.FloodWait as wait_err:
                    logger.error(wait_err)
                    logger.info(f"Wait {wait_err.value}")
                    time.sleep(wait_err.value)
                except Exception as ext:
                    logger.exception(ext)
                    continue
    result = create_result_file(chat_members)
    return result


async def parser_by_geo(
    lat: float,
    lng: float,
    accuracy_radius: int,
    api_id: int,
    api_hash: str,
    session_string: str,
):
    logger.info("Start parse geo locate")

    nearby_users = dict()
    try:
        async with Client(
            ":memory:", api_id, api_hash, session_string=session_string
        ) as client:
            r = await client.invoke(
                functions.contacts.GetLocated(
                    geo_point=InputGeoPoint(
                        lat=lat, long=lng, accuracy_radius=accuracy_radius
                    ),
                    background=False,
                    self_expires=0x7FFFFFFF,
                )
            )
            for nearby_user in r.users:
                if isinstance(nearby_user, types.ChatMember):
                    if nearby_user.status == "left":
                        continue
                    user = nearby_user.user
                else:
                    user = nearby_user
                info = info_user_for_geo(user)
                if user.id not in nearby_users:
                    info["count"] = 1
                    nearby_users[user.id] = info
                else:
                    nearby_users[user.id]["count"] += 1
    except Exception as ex:
        logger.exception(ex)
        nearby_users = {"error": f"Error: {ex}"}
    result = create_result_file(nearby_users)
    return result
