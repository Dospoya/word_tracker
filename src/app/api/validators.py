from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.user import bot_user_crud
from src.app.crud.profile import profile_crud
from src.app.models import User, Profile
from src.app.schemas.user import UserCreate


async def validate_user_exists(
    tg_id: int,
    session: AsyncSession,
) -> User:
    existing_user = await bot_user_crud.get_user_by_tg_id(
        tg_id=tg_id,
        session=session,
    )
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Пользователь с tg_id: {tg_id} не найден',
        )
    return existing_user


async def validate_user_absent(
    user_in: UserCreate,
    session: AsyncSession,
) -> UserCreate:
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


async def validate_user_profile_exists(
    user_id: int,
    session: AsyncSession,
):
    existing_profile = await profile_crud.get(obj_id=user_id, session=session)
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Профиль пользователя с id: {user_id} уже существует',
        )
