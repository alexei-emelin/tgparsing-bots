from fastapi import APIRouter

import bot.views as views

bot_router = APIRouter()

bot_router.add_api_route(
    "/chatmembers", endpoint=views.chat_members, methods=["GET"], tags=["parsing"]
)

bot_router.add_api_route(
    "/byperiodmembers", endpoint=views.by_period_members, methods=["GET"], tags=["parsing"]
)

bot_router.add_api_route(
    "/geomembers", endpoint=views.geo_members, methods=["GET"], tags=["parsing"]
)

bot_router.add_api_route(
    "/privatemembers", endpoint=views.privat_members, methods=["GET"], tags=["parsing"]
)

bot_router.add_api_route(
    "/checkblock", endpoint=views.check_block, methods=["GET"], tags=["check account"]
)

bot_router.add_api_route(
    "/checkgeo", endpoint=views.check_geo, methods=["GET"], tags=["check account"]
)
