from typing import List
from fastapi import APIRouter
from schemas import ChatMember
import parsing


router = APIRouter()


@router.get("/chatmembers", response_model=List[ChatMember])
async def chat_members():
    return await parsing.parser_chat_members_by_subscribes()


@router.get("/membersbyperiod", response_model=List[ChatMember])
async def chat_members_by_period():
    return await parsing.parser_chat_members_by_period()


@router.get("/privatechat", response_model=List[ChatMember])
async def private_channel():
    return await parsing.parser_private_channel()


@router.get("/usersnearby", response_model=List[ChatMember])
async def users_nearby():
    return await parsing.parser_by_geo()
