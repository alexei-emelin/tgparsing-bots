from fastapi import APIRouter

from bot.routes import bot_router

router = APIRouter()

router.include_router(bot_router, prefix="/bot")
