from pydantic import BaseModel


class ChatMember(BaseModel):
    id: int
    firstname: str
    lastname: str
    phone: str
    username: str
