import asyncio
import datetime
import json
import os
import time
import typing

from pyrogram import Client, types, enums
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


def create_result_file(data: typing.Dict, chat_name):
    os.makedirs("files", exist_ok=True)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    file_name = f"files/{chat_name}_{timestr}.json"
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
            # TODO проверку на тип чата - сделал Стас (надо порефакторить if)
            chat = await client.get_chat(chat_name)
            if chat.type is enums.ChatType.CHANNEL:
                channel = []
                channel.append(chat_name)
                await parser_private_channel(
                    channel, api_id, api_hash, session_string
                )
            else:
                _chat_members = [
                    x async for x in client.get_chat_members(chat_name)
                ]
                for chat_member in _chat_members:
                    user = chat_member.user
                    info = info_user(user)
                    if user.id not in chat_members:
                        info["count"] = 1
                        chat_members[user.id] = info
                    else:
                        chat_members[user.id]["count"] += 1
                create_result_file(chat_members, chat_name)
            

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
        # TODO проверку на тип чата
        for chat_name in parsered_chats:
            _chat_members = []
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
                    _chat_members.append(message.from_user)
         
                for chat_member in _chat_members:
                    user = chat_member
                    info = info_user(user)
                    if user.id not in chat_members:
                        info["count"] = 1
                        chat_members[user.id] = info
                    else:
                        chat_members[user.id]["count"] += 1
            create_result_file(chat_members, chat_name)


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
            # TODO for tests use
            # TODO history_messages = [x async for x in client.get_chat_history(chat_id=chat_name, limit=10)]
            history_messages = [
                x async for x in client.get_chat_history(chat_id=chat_name, limit=5)
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
        create_result_file(chat_members, chat_name)


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
        for user in r.users:
            info = info_user_for_geo(user)
            if user.id not in nearby_users:
                info["count"] = 1
                nearby_users[user.id] = info
            else:
                nearby_users[user.id]["count"] += 1
    name = f"geopars_rad_{accuracy_radius}"
    return create_result_file(nearby_users, name)
