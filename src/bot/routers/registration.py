from aiogram import Router

from bot.handlers.applicant.registration import registration_router

registration_routers = Router()
_ = registration_routers.include_router(router=registration_router)
