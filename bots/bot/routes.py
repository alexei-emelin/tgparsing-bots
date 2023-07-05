from fastapi import APIRouter

from bot import views


parser_router = APIRouter(tags=["Parser"])

parser_router.add_api_route(
    "/members",
    endpoint=views.get_chat_members,
    methods=["GET"],
    description="Получение пользователей из списка групп",
)
parser_router.add_api_route(
    "/geomembers",
    endpoint=views.get_members_by_geo,
    methods=["GET"],
    description="Получение пользователей по геолокации",
)
parser_router.add_api_route(
    "/chats",
    endpoint=views.get_chats,
    methods=["GET"],
    description="Получение групп по ключевому слову",
)
# parser_router.add_api_route(
#     "/byperiodmembers",
#     endpoint=views.by_period_members,
#     methods=["GET"],
#     tags=["parsing"],
# )
#
# parser_router.add_api_route(
#     "/privatemembers",
#     endpoint=views.privat_members,
#     methods=["GET"],
#     tags=["parsing"],
# )
# parser_router.add_api_route(
#     "/checkblock",
#     endpoint=views.check_block,
#     methods=["GET"],
#     tags=["check account"],
# )
# parser_router.add_api_route(
#     "/checkgeo",
#     endpoint=views.check_geo,
#     methods=["GET"],
#     tags=["check account"],
# )
