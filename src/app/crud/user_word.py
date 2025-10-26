from collections.abc import Sequence

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.global_word import GlobalWord
from app.models.user_word import UserWord
from app.schemas.user_word import UserWordCreate, UserWordUpdate


class CRUDUserWord(CRUDBase[UserWord, UserWordCreate, UserWordUpdate]):
    async def get_words_by_profile(
        self,
        pid: int,
        session: AsyncSession,
    ) -> Sequence[UserWord]:
        query = await session.execute(
            select(UserWord)
            .where(UserWord.profile_id == pid)
            .options(selectinload(UserWord.global_word))
            .order_by(UserWord.added_at.desc())
        )
        return query.scalars().all()

    async def get_words_by_user_id(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> Sequence[UserWord]:
        query = await session.execute(
            select(UserWord)
            .where(UserWord.user_id == user_id)
            .options(selectinload(UserWord.global_word))
            .order_by(UserWord.added_at.desc())
        )
        return query.scalars().all()

    async def has(
        self,
        user_id: int,
        word: str,
        session: AsyncSession,
    ) -> UserWord | None:
        lemma = word.strip().lower()
        result = await session.execute(
            select(UserWord)
            .join(GlobalWord, GlobalWord.id == UserWord.word_id)
            .where((UserWord.user_id == user_id) & (GlobalWord.word == lemma))
        )
        return result.scalar_one_or_none()

    async def add(
        self,
        user_id: int,
        profile_id: int,
        word_id: int,
        session: AsyncSession,
    ) -> bool:
        result = (
            await session.execute(
                insert(UserWord)
                .values(user_id=user_id, profile_id=profile_id, word_id=word_id)
                .on_conflict_do_nothing(constraint="unique_word_user")
                .returning(UserWord)
            )
        ).scalar_one_or_none()
        created = result is not None
        if created:
            _ = await session.execute(
                update(GlobalWord)
                .where(GlobalWord.id == word_id)
                .values(count=GlobalWord.count + 1)
            )
        await session.commit()
        return created


user_word_crud = CRUDUserWord(UserWord)
