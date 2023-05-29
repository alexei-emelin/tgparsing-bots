from fastapi import APIRouter
from bot import routes as bot_routes


router = APIRouter()

router.include_router(bot_routes.router, prefix="/bot")