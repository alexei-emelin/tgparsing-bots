import binascii
import typing

import bot.parsing as ps
import fastapi as fa
from bot import schemas as bot_sh
from pyrogram import Client


async def get_chat_members(body_data: bot_sh.PostBase) -> typing.Any:
    data = body_data.dict()
    session_string = data.pop("session_string")
    try:
        async with Client("account", session_string=session_string) as client:
            members = await ps.members_parser(
                client,
                **data,
            )
        return members
    except binascii.Error as exc:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_409_CONFLICT, detail=str(exc)
        )


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
            status_code=fa.status.HTTP_409_CONFLICT, detail=str(exc)
        )


async def get_members_by_geo(
    body_data: bot_sh.GetByGeo,
) -> dict:
    try:
        async with Client(
            "account", session_string=body_data.session_string
        ) as client:
            all_members = await ps.mass_get_by_geo(
                client, body_data.coordinates, body_data.accuracy_radius
            )
        return all_members
    except binascii.Error as exc:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_409_CONFLICT, detail=str(exc)
        )


async def get_chats(
    body_data: bot_sh.GetChats,
) -> list:
    async with Client(
        "account", session_string=body_data.session_string
    ) as client:
        chats = await ps.parser_search_chats(client, body_data.query)
    return chats
