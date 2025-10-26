import contextlib

from fastapi_users.exceptions import UserAlreadyExists

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.models.user import UserRole
from app.schemas.user import UserCreate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_first_superuser() -> None:
    async with get_async_session_context() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                try:
                    user = UserCreate(
                        email=settings.first_superuser_email,
                        password=settings.first_superuser_password,
                        first_name=settings.first_superuser_first_name,
                        tg_id=settings.first_superuser_tg_id,
                        role=UserRole.ADMIN,
                    )
                    _ = await user_manager.create(user, safe=True)
                    print(
                        f"Superuser {settings.first_superuser_email} created",
                    )
                except UserAlreadyExists:
                    print(
                        f"Superuser {settings.first_superuser_email} already exists",
                    )
