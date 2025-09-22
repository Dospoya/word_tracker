from fastapi import APIRouter

from src.app.api.endpoints import bot_router, profile_router, user_router


main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(
    bot_router, prefix='/bot', tags=['Bot'],
)
main_router.include_router(
    profile_router, prefix='/profile', tags=['Profile'],
)
