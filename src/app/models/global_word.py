from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, IdMixin

if TYPE_CHECKING:
    from app.models.user_word import UserWord

MAX_WORD_LEN = 128


class GlobalWord(Base, IdMixin):
    word: Mapped[str] = mapped_column(String(MAX_WORD_LEN), nullable=False, unique=True)
    meanings: Mapped[list[dict[str, str | list[str]]]] = mapped_column(
        JSONB, default=list, nullable=False
    )
    antonyms: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    synonyms: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, doc="Количество добавлений слова"
    )
    user_words: Mapped[list["UserWord"]] = relationship(
        "UserWord",
        back_populates="global_word",
    )

    def __repr__(self) -> str:
        return f"{self.word}."
