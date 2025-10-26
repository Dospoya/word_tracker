from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, IdMixin

if TYPE_CHECKING:
    from app.models.global_word import GlobalWord
    from app.models.profile import Profile

MAX_WORD_LEN = 128


class WordStatus(str, Enum):
    NEW = "new"
    LEARNING = "learning"
    MASTERED = "mastered"


class UserWord(Base, IdMixin):
    word_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("globalword.id"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    profile_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profile.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String, default=WordStatus.NEW)
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    global_word: Mapped["GlobalWord"] = relationship(
        "GlobalWord", back_populates="user_words", lazy="joined"
    )
    profile: Mapped["Profile"] = relationship("Profile", back_populates="words")

    __table_args__ = (UniqueConstraint("word_id", "user_id", name="unique_word_user"),)

    def __repr__(self) -> str:
        return f"{self.global_word.word}"
