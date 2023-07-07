import fastapi as fa
from pyrogram import Client

import bot.parsing as ps


async def get_chat_members(
    session_string: str,
    parsed_chats: list = fa.Query(),
) -> list:
    async with Client("account", session_string=session_string) as client:
        members = await ps.members_parser(client, parsed_chats)
    return members


async def get_members_by_geo(
    session_string: str,
    latitude: float,
    longitude: float,
    accuracy_radius: int = fa.Query(description="In meters"),
) -> list:
    async with Client("account", session_string=session_string) as client:
        if not client.me.photo:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_400_BAD_REQUEST,
                detail="У аккаунта должна быть аватарка",
            )
        members = await ps.parser_by_geo(
            client, latitude, longitude, accuracy_radius
        )
    return members


async def get_chats(
    session_string: str,
    query: str = fa.Query(description="Ключевое слово"),
):
    async with Client("account", session_string=session_string) as client:
        chats = await ps.parser_search_chats(client, query)
    return chats


# async def by_period_members(
#     api_id: int,
#     api_hash: str,
#     session_string: str,
#     period_from: datetime.date,
#     period_to: datetime.date,
#     parsered_chats: list = fa.Query(),
# ) -> list:
#     period_from_ = datetime.datetime.fromisoformat(period_from.isoformat())
#     period_to_ = datetime.datetime.fromisoformat(period_to.isoformat())
#     period_to_ += datetime.timedelta(days=1)
#
#     return await ps.start_parser_by_period(
#         parsered_chats,
#         period_from_,
#         period_to_,
#         api_id,
#         api_hash,
#         session_string,
#     )
#

# async def geo_members(
#     lat: float,
#     lng: float,
#     accuracy_radius: int,
#     api_id: int,
#     api_hash: str,
#     session_string: str,
# ) -> list:
#     return await ps.parser_by_geo(
#         lat, lng, accuracy_radius, api_id, api_hash, session_string
#     )
#
#
# async def privat_members(
#     api_id: int,
#     api_hash: str,
#     session_string: str,
#     parsered_chats: list = fa.Query(),
#     limit: int = 500,
# ) -> list:
#     return await ps.start_parser_privat_chanels(
#         parsered_chats, api_id, api_hash, session_string, limit
#     )
#
#
# async def check_block(
#     api_id: int, api_hash: str, session_string: str
# ) -> bool:
#     return await check_account_on_block(api_id, api_hash, session_string)
#
#
# async def check_geo(api_id: int, api_hash: str, session_string: str) -> bool:
#     return await check_account_by_geo(api_id, api_hash, session_string)
