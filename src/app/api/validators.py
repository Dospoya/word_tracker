from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.global_word import global_word_crud
from app.crud.profile import profile_crud
from app.crud.user import bot_user_crud
from app.crud.user_word import user_word_crud
from app.models.user import User
from app.schemas.user import UserCreate


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
            detail=f"Пользователь с tg_id: {tg_id} не найден",
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
        detail=f"Пользователь с tg_id: {user_in.tg_id} уже существует",
    )


async def validate_user_profile_absent(
    user_id: int,
    session: AsyncSession,
):
    existing_profile = await profile_crud.get_profile_by_user_id(
        user_id=user_id, session=session
    )
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Профиль пользователя с id: {user_id} уже существует",
        )


async def validate_user_profile_exists(
    tg_id: int,
    session: AsyncSession,
):
    user = await validate_user_exists(tg_id, session)
    existing_profile = await profile_crud.get_profile_by_tg_id(
        tg_id=user.tg_id, session=session
    )
    if not existing_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Профиль пользователя с tg_id: {user.tg_id} не найден",
        )
    return existing_profile


async def validate_word_exists_in_db(word: str, session: AsyncSession):
    existing_word = await global_word_crud.get_word(word, session)
    if not existing_word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Введенное слово {word} не найдено",
        )
    return existing_word


async def validate_word_exists_in_user_list(
    user_id: int, word: str, session: AsyncSession
):
    existing_word = await user_word_crud.has(user_id, word, session)
    if not existing_word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Слово {word} не найдено в списке пользователя с id: {user_id}",
        )
    return existing_word
