from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.global_word import GlobalWord
from app.schemas.global_word import GlobalWordCreate, GlobalWordUpdate


class CRUDGlobalWord(CRUDBase[GlobalWord, GlobalWordCreate, GlobalWordUpdate]):
    async def get_word(self, word: str, session: AsyncSession) -> GlobalWord | None:
        word = word.strip().lower()
        result = await session.execute(
            select(GlobalWord).where(GlobalWord.word == word)
        )
        return result.scalar_one_or_none()


global_word_crud = CRUDGlobalWord(GlobalWord)
