from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models import Profile, User
from .base import CRUDBase


class ProfileCRUD(CRUDBase):
    async def get_profile_by_tg_id(
        self,
        tg_id: int,
        session: AsyncSession,
    ):
        profile = await session.execute(
            select(Profile)
            .join(User)
            .where(
                User.tg_id == tg_id
            )
        )
        return profile.scalar_one_or_none()


profile_crud = ProfileCRUD(Profile)
