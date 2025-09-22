from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.models import GlobalWord, Profile, User, UserWord
from src.app.crud.base import CRUDBase

class CRUDWord(CRUDBase):
    async def get_words_by_pid(
        self,
        pid: int,
        session: AsyncSession,
    ) -> Sequence[GlobalWord]:
        query = await session.execute(
            select(UserWord)
            .where(UserWord.profile_id == pid)
            .options(selectinload(UserWord.global_word))
            .order_by(UserWord.added_at.desc())
        )
        return query.scalars().all()

    async def get_word(
        self,
        word: str,
        session: AsyncSession
    ) -> GlobalWord:
        result = await session.execute(
            select(GlobalWord).where(GlobalWord.word == word)
        )
        return result.scalar_one_or_none()

word_crud = CRUDWord(GlobalWord)
