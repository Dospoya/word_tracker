from aiogram import Router
from aiogram.filters import Command

from bot.handlers import start
from bot.routers.registration import registration_routers
from bot.routers.user import user_router

main_router = Router()
_ = main_router.message.register(start.start_handler, Command(commands=["start"]))
_ = main_router.include_router(router=registration_routers)
_ = main_router.include_router(router=user_router)
