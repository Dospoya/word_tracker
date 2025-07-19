from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db import get_async_session
from src.app.core.user import auth_backend, current_superuser, fastapi_users
from src.app.models import User
from src.app.schemas.user import (
    UserCreate,
    UserDB,
    UserUpdate,
)

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

router.include_router(
    fastapi_users.get_register_router(UserDB, UserCreate),
    prefix='/auth',
    tags=['auth'],
)


router.include_router(
    fastapi_users.get_users_router(UserDB, UserUpdate),
    prefix='/users',
    tags=['users'],
)


@router.get("/users/",
            response_model=List[UserDB],
            tags=['users'],
            dependencies=[Depends(current_superuser)])
async def get_all_users(
        tg_id: Optional[int] = None,
        session: AsyncSession = Depends(get_async_session),
) -> List[UserDB]:
    query = select(User)
    if tg_id is not None:
        query = query.where(User.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalars().all()
