from fastapi import APIRouter

import bot.views as views


bot_router = APIRouter()

bot_router.add_api_route(
    "/chatmembers", endpoint=views.chat_members, methods=['GET']
)

bot_router.add_api_route(
    "/byperiodmembers", endpoint=views.by_period_members, methods=['GET']
)

bot_router.add_api_route(
    "/geomembers", endpoint=views.geo_members, methods=['GET']
)

bot_router.add_api_route(
    "/privatemembers", endpoint=views.privat_members, methods=['GET']
)
