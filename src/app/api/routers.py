from fastapi import APIRouter

from app.api.endpoints import bot_router, user_router


main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(
    bot_router, prefix='/bot', tags=['Bot'],
)
