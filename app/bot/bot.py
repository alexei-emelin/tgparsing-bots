# from pyrogram import Client
#
# # from utils.log_func import logger
# from bot.utils.log_func import logger
#
# # api_id = config.API_ID
# # api_hash = config.API_HASH
# # workdir = os.path.join(os.path.dirname(__file__), "sessions")
# # phone_number = config.PHONE_NUMBER
#
#
# async def check_account_on_block(
#     api_id: int, api_hash: str, session_string: str
# ) -> bool:
#     logger.info("start check account on block")
#     async with Client(
#         ":memory:", api_id, api_hash, session_string=session_string
#     ) as client:
#         acc_info = await client.get_me()
#
#     return (
#         acc_info.is_scam
#         or acc_info.is_restricted
#         or acc_info.is_fake
#         or acc_info.is_bot
#     )
#
#
# async def check_account_by_geo(
#     api_id: int, api_hash: str, session_string: str
# ) -> bool:
#     logger.info("start check account by geo")
#     async with Client(
#         ":memory:", api_id, api_hash, session_string=session_string
#     ) as client:
#         count_profile_photos = await client.get_chat_photos_count("me")
#     return bool(count_profile_photos)
#
#
# # async def get_work_accounts(accounts: typing.List[typing.Dict]):
# #     pass
