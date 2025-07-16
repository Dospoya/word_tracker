from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserDB
)
from app.api.validators import check_user_exists_by_tg_id
from app.core.db import get_async_session
from app.core.security import verify_bot_token
from app.core.user import get_user_manager, UserManager

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
    user = await check_user_exists_by_tg_id(user_in, session)
    return await user_manager.create(user)
