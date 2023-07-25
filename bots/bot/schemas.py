from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class GetChats(BaseModel):
    session_string: str
    query: str = Field(description="Ключевое слово")


class PostBase(BaseModel):
    session_string: str
    parsed_chats: List[str] = Field(
        description="Список чатов для парсинга",
    )
    groups_count: int


class Activity(BaseModel):
    comments: bool
    reposts: bool


class GetActiveMembers(BaseModel):
    session_string: str
    parsed_chats: List[str] = Field(
        description="Список чатов для парсинга",
    )
    from_date: datetime
    to_date: datetime
    activity_count: int
    activity: Activity


class GetByGeo(BaseModel):
    session_string: str
    latitude: float
    longitude: float
    accuracy_radius: int = Field(description="In meters")


class MemberInfoResponse(BaseModel):
    first_name: str | None
    last_name: str | None
    username: str | None
    phone_number: str | None
    groups: List[str]
