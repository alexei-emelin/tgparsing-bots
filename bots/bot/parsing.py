import typing

from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.raw import functions, types

from bot import utils as ut
from settings import config


async def members_parser(
    client: Client,
    parsed_chats: typing.List[str],
) -> typing.List[dict]:
    all_data = []
    for parsed_chat in parsed_chats:
        chat = await ut.get_group_info(client, parsed_chat)
        if not chat or chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            continue
        members_gen = client.get_chat_members(
            chat_id=parsed_chat,
        )
        chat_members = {
            "chat": {
                "title": chat.title,
                "description": chat.description,
                "username": chat.username,
            },
            "members": [
                ut.get_member_info(member.user)
                async for member in members_gen
                if not member.user.is_bot
            ]
            if members_gen
            else [],
        }
        all_data.append(chat_members)
    return all_data


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
        ut.get_geomember_info(member)
        for member in resp_members.users
        if not member.bot
    ]
    return members


async def parser_search_chats(
    client: Client,
    query: str,
):
    chats_resp = await client.invoke(
        functions.contacts.Search(q=query, limit=config.SEARCH_LIMIT)
    )
    chats = [ut.get_chat_info(item) for item in chats_resp.chats]
    return chats


# async def parser_chat_members_by_period(
#     chat_name: str,
#     period_from: datetime.date,
#     period_to: datetime.date,
#     api_id: int,
#     api_hash: str,
#     session_string: str,
# ):
#     logger.info("Parser chat members by period")
#     chat_members = {}
#     async with Client(
#         ":memory:", api_id, api_hash, session_string=session_string
#     ) as client:
#         members_list = []
#         history_messages = [
#             x
#             async for x in client.get_chat_history(
#                 chat_id=chat_name, offset_date=period_to, limit=2000
#             )
#         ]
#         for message in history_messages:
#             if message.date < period_from:
#                 continue
#             if message.from_user:
#                 members_list.append(message.from_user)
#
#             for chat_member in members_list:
#                 user = chat_member
#                 info = get_member_info(user)
#                 if user.id not in chat_members:
#                     info["count"] = 1
#                     chat_members[user.id] = info
#                 else:
#                     chat_members[user.id]["count"] += 1
#     # file_path = create_result_file(chat_members, chat_name)
#     return
#
#
# async def start_parser_by_period(
#     parsered_chats: typing.List[str],
#     period_from: datetime.date,
#     period_to: datetime.date,
#     api_id: int,
#     api_hash: str,
#     session_string: str,
# ) -> typing.List[str]:
#     file_paths_list = []
#     for chat in parsered_chats:
#         chat_type = await get_group_info(chat, api_id)
#         if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]:
#             file_path = await parser_chat_members_by_period(
#                 chat, period_from,
#                 period_to, api_id,
#                 api_hash, session_string
#             )
#             file_paths_list.append(file_path)
#         else:
#             info_text = f"""
#             {chat} не является чатом, проверьте правильность ссылки, \
#             либо воспользуйтесь другой услугой
#             """
#             answer = {"error": textwrap.dedent(info_text).strip()}
#             # file_path = create_result_file(answer, chat)
#             # file_paths_list.append(file_path)
#     return []
#
#
# async def parser_private_channel(
#     chat_name: str,
#     api_id: int,
#     api_hash: str,
#     session_string: str,
#     limit: int
# ):
#     chat_members = {}
#     async with Client(
#         ":memory:", api_id, api_hash, session_string=session_string
#     ) as client:
#         history_messages = [
#             x
#             async for x in client.get_chat_history(
#                 chat_id=chat_name, limit=limit
#             )
#         ]
#         for message in history_messages:
#             try:
#                 discussion_replies = [
#                     x
#                     async for x in client.get_discussion_replies(
#                         chat_name, message.id
#                     )
#                 ]
#                 for comment in discussion_replies:
#                     if not comment.from_user.is_bot:
#                         info = get_member_info(comment.from_user)
#                         if comment.from_user.id not in chat_members:
#                             info["count"] = 1
#                             chat_members[comment.from_user.id] = info
#                         else:
#                             chat_members[comment.from_user.id]["count"] += 1
#             except bad_request_400.MsgIdInvalid:
#                 logger.error("Не удалось получить комментарии к посту")
#                 continue
#             except flood_420.FloodWait as wait_err:
#                 logger.error(wait_err)
#                 logger.info("Wait %s", wait_err.value)
#                 time.sleep(wait_err.value)
#     # file_path = create_result_file(chat_members, chat_name)
#     return
#
#
# async def start_parser_privat_chanels(
#     parsered_chats: typing.List[str],
#     api_id: int,
#     api_hash: str,
#     session_string: str,
#     limit: int,
# ) -> typing.List[str]:
#     file_paths_list = []
#     for chat in parsered_chats:
#         chat_type = await get_group_info(chat, api_id)
#         if chat_type == ChatType.CHANNEL:
#             file_path = await parser_private_channel(
#                 chat, api_id, api_hash, session_string, limit
#             )
#             file_paths_list.append(file_path)
#         else:
#             info_text = f"""
#             {chat} не является каналом, проверьте правильность ссылки, \
#             либо воспользуйтесь другой услугой
#             """
#             result = {"error": textwrap.dedent(info_text).strip()}
#             # file_path = create_result_file(result, chat)
#             # file_paths_list.append(file_path)
#     return []
