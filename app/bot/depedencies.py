from fastapi import HTTPException, Request, status
from settings import config


def check_ip(request: Request):
    if request.client:
        host = request.client.host
        if host == config.ALLOWED_HOST:
            return
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Фи пароли, мазафака!",
    )
