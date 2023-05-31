import asyncio
import datetime
from typing import List
from fastapi import APIRouter, Query
from .parsing import parser_by_geo, parser_chat_members_by_period, parser_chat_members_by_subscribes, parser_private_channel
from .schemas import ChatMember

from bot.utils.log_func import logger

bot_router = APIRouter()


# @router.get("/chatmembers", response_model=List[ChatMember])
@bot_router.get("/chatmembers")
async def chat_members(api_id: int,
                       api_hash: str,
                       session_string: str,
                       parsered_chats: list = Query()):
    return await parser_chat_members_by_subscribes(parsered_chats,
                                                   api_id,
                                                   api_hash,
                                                   session_string)


@bot_router.get("/membersbyperiod")
async def chat_members_by_period(api_id: int,
                                 api_hash: str,
                                 session_string: str,
                                 period_from: datetime.date,
                                 period_to: datetime.date,
                                 parsered_chats: list = Query()):
    return await parser_chat_members_by_period(parsered_chats,
                                               period_from,
                                               period_to,
                                               api_id,
                                               api_hash,
                                               session_string)


@bot_router.get("/privatechat", response_model=List[ChatMember])
async def private_channel():
    return await parser_private_channel()


@bot_router.get("/usersnearby", response_model=List[ChatMember])
async def users_nearby():
    return await parser_by_geo()
