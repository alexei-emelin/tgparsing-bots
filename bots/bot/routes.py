from fastapi import APIRouter

from bot import views
from settings import config


parser_router = APIRouter(tags=["Parser"])

parser_router.add_api_route(
    "/members",
    endpoint=views.get_chat_members,
    methods=["POST"],
    description="Получение пользователей из списка групп",
)
parser_router.add_api_route(
    path="/activemembers",
    endpoint=views.get_active_members,
    methods=["POST"],
    name=config.PARSER_ACTIVE_MEMBERS,
    description="Получить всех пользователей из списка групп, "
    "которые проявляли активность за определенный период",
)
parser_router.add_api_route(
    "/geomembers",
    endpoint=views.get_members_by_geo,
    methods=["POST"],
    description="Получение пользователей по геолокации",
)
parser_router.add_api_route(
    "/chats",
    endpoint=views.get_chats,
    methods=["POST"],
    description="Получение групп по ключевому слову",
)
