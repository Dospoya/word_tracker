# from typing import Sequence

# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession

# from src.app.models import Word, User, Profile
# from src.app.crud.base import CRUDBase

# class CRUDWord(CRUDBase):
#     async def get_words_by_user_tg_id(
#         self,
#         tg_id: int,
#         session: AsyncSession,
#     ) -> Sequence[Word]:
#         query = await session.execute(
#             select(Word)
#             .join(Word.profile)
#             .join(Profile.user)
#             .where(User.tg_id == tg_id)
#         )
#         return query.scalars().all()

# word_crud = CRUDWord(Word)
