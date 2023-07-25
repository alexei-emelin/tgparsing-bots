import binascii
import typing

import fastapi as fa
from pyrogram import Client

import bot.parsing as ps
from bot import schemas as bot_sh
from bot import utils as bot_ut


async def get_chat_members(body_data: bot_sh.PostBase) -> typing.Any:
    async with Client(
        "account", session_string=body_data.session_string
    ) as client:
        members = await ps.members_parser(
            client, body_data.parsed_chats, body_data.groups_count
        )
    return members


async def get_active_members(body_data: bot_sh.GetActiveMembers) -> dict:
    data = body_data.dict()
    session_string = data.pop("session_string")
    try:
        async with Client("account", session_string=session_string) as client:
            members = await ps.get_active_members(
                client=client,
                **data,
            )
        return members
    except binascii.Error as exc:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_409_CONFLICT,
            detail=str(exc)
        )


async def get_members_by_geo(
    body_data: bot_sh.GetByGeo,
) -> list:
    async with Client(
        "account", session_string=body_data.session_string
    ) as client:
        if not client.me.photo:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_400_BAD_REQUEST,
                detail="У аккаунта должна быть аватарка",
            )
        members = await ps.parser_by_geo(
            client,
            body_data.latitude,
            body_data.longitude,
            body_data.accuracy_radius,
        )
    return members


async def get_chats(
    body_data: bot_sh.GetChats,
) -> list:
    async with Client(
        "account", session_string=body_data.session_string
    ) as client:
        chats = await ps.parser_search_chats(client, body_data.query)
    return chats
