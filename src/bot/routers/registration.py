from aiogram import Router

from src.bot.handlers.applicant.registration import registration_router

registration_routers = Router()
registration_routers.include_router(router=registration_router)
