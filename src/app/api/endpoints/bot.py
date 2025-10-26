from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    validate_user_absent,
    validate_user_exists,
    validate_user_profile_absent,
    validate_user_profile_exists,
    validate_word_exists_in_db,
    validate_word_exists_in_user_list,
)
from app.core.db import get_async_session
from app.core.security import verify_bot_token
from app.core.user import UserManager, get_user_manager
from app.crud.profile import profile_crud
from app.crud.user_word import user_word_crud
from app.schemas.global_word import GlobalWordDB
from app.schemas.profile import (
    ProfileCreate,
    ProfileDB,
)
from app.schemas.user import UserCreate, UserDB
from app.schemas.user_word import (
    UserWordCreate,
    UserWordCreateResponse,
    UserWordDetail,
)

router = APIRouter()


@router.post(
    "/users",
    response_model=UserDB,
    dependencies=[Depends(verify_bot_token)],
)
async def create_user(
    user_in: UserCreate,
    user_manager: Annotated[UserManager, Depends(get_user_manager)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    user = await validate_user_absent(user_in, session)
    return await user_manager.create(user)


@router.post(
    "/users/profile",
    response_model=ProfileDB,
    dependencies=[Depends(verify_bot_token)],
)
async def create_profile(
    user_profile: ProfileCreate,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    await validate_user_profile_absent(user_id=user_profile.user_id, session=session)
    return await profile_crud.create(user_profile, session)


@router.get(
    "/users/{tg_id}/profile",
    response_model=ProfileDB,
    dependencies=[Depends(verify_bot_token)],
)
async def get_profile_info_by_tg_id(
    tg_id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return await validate_user_profile_exists(tg_id, session)


@router.get(
    "/users/{tg_id}",
    response_model=UserDB,
    dependencies=[Depends(verify_bot_token)],
)
async def get_user_by_tg_id(
    tg_id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return await validate_user_exists(tg_id, session)


@router.post(
    "/users/{tg_id}/add_word",
    response_model=UserWordCreateResponse,
    dependencies=[Depends(verify_bot_token)],
)
async def add_word_to_user(
    tg_id: int,
    user_word: UserWordCreate,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    user = await validate_user_exists(tg_id, session)
    profile = await validate_user_profile_exists(tg_id, session)
    word = await validate_word_exists_in_db(user_word.word, session)
    result = await user_word_crud.add(user.id, profile.id, word.id, session)
    if not result:
        return {"created": False}
    return {"created": True}


@router.get(
    "/users/{tg_id}/words/{word}",
    response_model=UserWordDetail | None,
    dependencies=[Depends(verify_bot_token)],
)
async def get_user_word(
    tg_id: int,
    word: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    user = await validate_user_exists(tg_id, session)
    return await validate_word_exists_in_user_list(user.id, word, session)


@router.get(
    "/users/{tg_id}/words",
    response_model=list[UserWordDetail],
    dependencies=[Depends(verify_bot_token)],
)
async def get_words_by_tg_id(
    tg_id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    user = await validate_user_exists(tg_id, session)
    return await user_word_crud.get_words_by_user_id(user.id, session)


@router.get(
    "/words/{word}",
    response_model=GlobalWordDB,
    dependencies=[Depends(verify_bot_token)],
)
async def get_global_word(
    word: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return await validate_word_exists_in_db(word, session)
