import asyncio
from typing import List
from fastapi import APIRouter, Query

from views import chat_members
from .parsing import parser_by_geo, parser_chat_members_by_period, parser_chat_members_by_subscribes, parser_private_channel
from .schemas import ChatMember


bot_router = APIRouter()

bot_router.add_api_route(
    "/chatmembers", endpoint=chat_members, methods=['GET']
)


@bot_router.get("/membersbyperiod", response_model=List[ChatMember])
async def chat_members_by_period():
    return await parser_chat_members_by_period()


@bot_router.get("/privatechat", response_model=List[ChatMember])
async def private_channel():
    return await parser_private_channel()


@bot_router.get("/usersnearby", response_model=List[ChatMember])
async def users_nearby():
    return await parser_by_geo()
