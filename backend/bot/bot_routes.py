import asyncio
from typing import List
from fastapi import APIRouter, Query
from .parsing import parser_by_geo, parser_chat_members_by_period, parser_chat_members_by_subscribes, parser_private_channel
from .schemas import ChatMember

router = APIRouter()


# @router.get("/chatmembers", response_model=List[ChatMember])
@router.get("/chatmembers")
async def chat_members(api_id: int,
                       api_hash: str,
                       session_string: str,
                       parsered_chats: list = Query()):
    return await parser_chat_members_by_subscribes(parsered_chats,
                                                   api_id,
                                                   api_hash,
                                                   session_string)


@router.get("/membersbyperiod", response_model=List[ChatMember])
async def chat_members_by_period():
    return await parser_chat_members_by_period()


@router.get("/privatechat", response_model=List[ChatMember])
async def private_channel():
    return await parser_private_channel()


@router.get("/usersnearby", response_model=List[ChatMember])
async def users_nearby():
    return await parser_by_geo()
