from pydantic import BaseModel


class ChatMember(BaseModel):
    id: int
    firstname: str | None = None
    lastname: str | None = None
    phone: str | None = None
    username: str
