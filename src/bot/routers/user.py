from aiogram import Router

from bot.handlers.user.service import service_router
from bot.handlers.user.vocab import vocabulary_router

user_router = Router()
_ = user_router.include_router(vocabulary_router)
_ = user_router.include_router(service_router)
