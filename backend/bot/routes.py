from typing import List
from fastapi import APIRouter
from bot.parsing import parser_by_geo, parser_chat_members_by_period, parser_chat_members_by_subscribes, parser_private_channel
from bot.schemas import ChatMember

router = APIRouter()


@router.get("/chatmembers", response_model=List[ChatMember])
async def chat_members():
    return await parser_chat_members_by_subscribes()


@router.get("/membersbyperiod", response_model=List[ChatMember])
async def chat_members_by_period():
    return await parser_chat_members_by_period()


@router.get("/privatechat", response_model=List[ChatMember])
async def private_channel():
    return await parser_private_channel()


@router.get("/usersnearby", response_model=List[ChatMember])
async def users_nearby():
    return await parser_by_geo()
