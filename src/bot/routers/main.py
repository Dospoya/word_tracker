from aiogram import Router
from aiogram.filters import Command

from src.bot.handlers import start
from src.bot.routers.registration import registration_routers

main_router = Router()
main_router.message.register(start.start_handler, Command(commands=['start']))
main_router.include_router(router=registration_routers)
