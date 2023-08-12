import fastapi
from fastapi import Request
from settings import config


def check_ip(request: Request):
    if request.client:
        host = request.client.host
        port = request.client.port
        print(f"-------->Важная инфа<-------{host}, {port}")
        if host == config.ALLOWED_HOST:
            return
    raise fastapi.HTTPException(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        detail="Фи пароли, мазафака!",
    )
