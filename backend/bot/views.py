from fastapi import Query

from parsing import parser_chat_members_by_subscribes


async def chat_members(api_id: int,
                       api_hash: str,
                       session_string: str,
                       parsered_chats: list = Query()):
    return await parser_chat_members_by_subscribes(parsered_chats,
                                                   api_id,
                                                   api_hash,
                                                   session_string)
