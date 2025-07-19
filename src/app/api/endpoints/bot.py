from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from src.app.models.profile import (
    EnglishVariant,
    EnglishLevel,
)
from src.app.schemas.profile import (
    ProfileCreate,
    ProfileDB,
)
from src.app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserDB
)
from src.app.api.validators import (
    validate_user_absent,
    validate_user_exists,
    validate_user_profile_exists,
)
from src.app.core.db import get_async_session
from src.app.core.security import verify_bot_token
from src.app.core.user import get_user_manager, UserManager
from src.app.crud.profile import profile_crud

router = APIRouter()


@router.post(
    '/users',
    response_model=UserDB,
    dependencies=[Depends(verify_bot_token)],
)
async def create_user(
    user_in: UserCreate,
    user_manager: UserManager = Depends(get_user_manager),
    session: AsyncSession = Depends(get_async_session)
):
    user = await validate_user_absent(user_in, session)
    return await user_manager.create(user)


@router.post(
    '/users/profile',
    response_model=ProfileDB,
    dependencies=[Depends(verify_bot_token)]
)
async def create_profile(
    user_profile: ProfileCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await validate_user_profile_exists(
        user_id=user_profile.user_id,
        session=session
    )
    return await profile_crud.create(user_profile, session)


@router.get(
    '/users/{tg_id}',
    response_model=UserDB,
    dependencies=[Depends(verify_bot_token)],
)
async def get_user_by_tg_id(
    tg_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await validate_user_exists(tg_id, session)
