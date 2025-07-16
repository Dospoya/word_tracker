from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models import User
from src.app.schemas.user import UserCreate, UserUpdate
from .base import CRUDBase

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_user_by_tg_id(
        self,
        session: AsyncSession,
        tg_id: int,
    ) -> User | None:
        query = select(User).where(User.tg_id == tg_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


bot_user_crud = CRUDUser(User)
