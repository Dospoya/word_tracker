from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.user import bot_user_crud
from src.app.crud.profile import profile_crud
from src.app.schemas.user import UserCreate


async def check_user_exists_by_tg_id(
    user_in: UserCreate,
    session: AsyncSession,
):
    existing_user = await bot_user_crud.get_user_by_tg_id(
        tg_id=user_in.tg_id,
        session=session,
    )
    if not existing_user:
        return user_in
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f'Пользователь с tg_id: {user_in.tg_id} уже существует',
    )


async def check_profile_exists(
    user_id: int,
    session: AsyncSession,
):
    existing_profile = await profile_crud.get(obj_id=user_id, session=session)
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Профиль пользователя с id: {user_id} уже существует',
        )
