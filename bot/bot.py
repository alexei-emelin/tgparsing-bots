import os
import typing
import asyncio

from pyrogram import Client

from config import logger


async def check_account(api_id: int, api_hash: str, session_string: str) -> bool:
    logger.info('start check account')
    with Client(':memory:',
                    api_id,
                    api_hash,
                    session_string=session_string,
                    in_memory=True) as client:
        acc_info = client.get_me()

    return acc_info.is_scam or acc_info.is_restricted or acc_info.is_fake or acc_info.is_bot


async def get_work_accounts(accounts: typing.List[typing.Dict]):
    pass
