from bot.routes import parser_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from settings import config


app = FastAPI(
    title=config.APP_NAME,
    docs_url=config.DOCS_URL,
    redoc_url=config.REDOC_URL,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.APP_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=config.APP_ALLOWED_HOSTS
)

app.include_router(parser_router)
