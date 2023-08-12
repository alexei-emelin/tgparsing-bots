import typing
from pathlib import Path

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    BASE_DIR: Path = Path(__file__).parent

    # server
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)
    ALLOWED_HOST: str = Field(default=None)

    APP_NAME: str = "TgBots"
    APP_ALLOWED_ORIGINS: typing.List[str] = Field(default=["*"])
    APP_ALLOWED_HOSTS: typing.List[str] = Field(default=["*"])
    DOCS_URL: typing.Optional[str] = Field(default=None)
    REDOC_URL: typing.Optional[str] = Field(default=None)

    # limits
    # parser
    SEARCH_LIMIT: int = Field(default=1000)

    # url names
    # static
    STATIC_DIR_NAME: str = Field(default="static")
    AVATARS_FOLDER: str = Field(default="bots_avatars")
    BASE_AVATAR_NAME: str = Field(default="base_avatar.jpg")

    @property
    def static_dir_url(self) -> Path:
        return Path(self.STATIC_DIR_NAME)

    @property
    def base_avatar_url(self) -> Path:
        return (
            self.BASE_DIR
            / self.static_dir_url
            / self.AVATARS_FOLDER
            / self.BASE_AVATAR_NAME
        )

    # parser
    PARSER_ACTIVE_MEMBERS: str = Field(default="parser_active_members")


config = Config()
