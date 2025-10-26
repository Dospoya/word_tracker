from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_user_by_tg_id(
        self,
        session: AsyncSession,
        tg_id: int,
    ) -> User | None:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        return result.scalar_one_or_none()

    async def get_users_by_role(
        self,
        session: AsyncSession,
        role: str,
    ) -> Sequence[User]:
        result = await session.execute(select(User).where(User.role == role))
        return result.scalars().all()


bot_user_crud = CRUDUser(User)
