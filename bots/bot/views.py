import datetime

from fastapi import Query

import bot.parsing as ps
from bot.bot import check_account_by_geo, check_account_on_block


async def chat_members(
    api_id: int,
    api_hash: str,
    session_string: str,
    parsered_chats: list = Query(),
) -> list:
    return await ps.start_parser_by_subscribes(
        parsered_chats, api_id, api_hash, session_string
    )


async def by_period_members(
    api_id: int,
    api_hash: str,
    session_string: str,
    period_from: datetime.date,
    period_to: datetime.date,
    parsered_chats: list = Query(),
) -> list:
    period_from_ = datetime.datetime.fromisoformat(period_from.isoformat())
    period_to_ = datetime.datetime.fromisoformat(period_to.isoformat())
    period_to_ += datetime.timedelta(days=1)

    return await ps.start_parser_by_period(
        parsered_chats,
        period_from_,
        period_to_,
        api_id,
        api_hash,
        session_string,
    )


async def geo_members(
    lat: float,
    lng: float,
    accuracy_radius: int,
    api_id: int,
    api_hash: str,
    session_string: str,
) -> list:
    return await ps.parser_by_geo(
        lat, lng, accuracy_radius, api_id, api_hash, session_string
    )


async def privat_members(
    api_id: int,
    api_hash: str,
    session_string: str,
    parsered_chats: list = Query(),
    limit: int = 500,
) -> list:
    return await ps.start_parser_privat_chanels(
        parsered_chats, api_id, api_hash, session_string, limit
    )


async def check_block(api_id: int, api_hash: str, session_string: str) -> bool:
    return await check_account_on_block(api_id, api_hash, session_string)


async def check_geo(api_id: int, api_hash: str, session_string: str) -> bool:
    return await check_account_by_geo(api_id, api_hash, session_string)
