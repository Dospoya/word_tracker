from .bot import router as bot_router
from .user import router as user_router
from .profile import router as profile_router

__all__ = [
    user_router,
    bot_router,
    profile_router,
]
