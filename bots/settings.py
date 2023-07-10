from pydantic import BaseSettings, Field


class Config(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    # server
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)

    UPLOADED_FILES_PATH = "media/"

    # tg
    API_ID: int = Field(default=0000)
    API_HASH: str = Field(default="YourTelegramHash")
    PHONE_NUMBER: str = Field(default="+00000000000")

    # limits
    # parser
    SEARCH_LIMIT: int = Field(default=1000)

    # url names
    # parser
    PARSER_MEMBERS: str = Field(default="parser_members")
    PARSER_ACTIVE_MEMBERS: str = Field(default="parser_active_members")


config = Config()
