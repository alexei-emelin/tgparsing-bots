from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bot.routes import parser_router


app = FastAPI(title="TgBots")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parser_router)
