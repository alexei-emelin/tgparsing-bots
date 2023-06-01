import datetime

from fastapi import Query

import bot.parsing as ps


async def chat_members(
    api_id: int,
    api_hash: str,
    session_string: str,
    parsered_chats: list = Query(),
):
    return await ps.parser_chat_members_by_subscribes(
        parsered_chats, api_id, api_hash, session_string
    )


async def by_period_members(
    api_id: int,
    api_hash: str,
    session_string: str,
    period_from: datetime.date,
    period_to: datetime.date,
    parsered_chats: list = Query(),
):
    return await ps.parser_chat_members_by_period(
        parsered_chats, period_from, period_to, api_id, api_hash, session_string
    )


async def geo_members(
    lat: float,
    lng: float,
    accuracy_radius: int,
    api_id: int,
    api_hash: str,
    session_string: str,
):
    return await ps.parser_by_geo(
        lat, lng, accuracy_radius, api_id, api_hash, session_string
    )


async def privat_members(
    api_id: int,
    api_hash: str,
    session_string: str,
    parsered_chats: list = Query(),
):
    return await ps.parser_private_channel(
        parsered_chats, api_id, api_hash, session_string
    )
