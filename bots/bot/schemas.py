from datetime import datetime, timedelta
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


class GetActiveMembers(PostBase):
    days: int = Field(
        ge=1,
        description="Количество дней. Если указан данный параметр, "
        "то период учитываться не будет",
    )
    from_date: datetime = Field(
        default=datetime.now().replace(microsecond=0) - timedelta(days=1)
    )
    to_date: datetime = Field(default=datetime.now().replace(microsecond=0))


class GetByGeo(BaseModel):
    session_string: str
    latitude: float
    longitude: float
    accuracy_radius: int = Field(description="In meters")
