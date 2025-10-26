from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, IdMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.user_word import UserWord


class EnglishVariant(str, Enum):
    AMERICAN = "american"
    BRITISH = "british"


class EnglishLevel(str, Enum):
    A1 = "a1"
    A2 = "a2"
    B1 = "b1"
    B2 = "b2"
    C1 = "c1"
    C2 = "c2"


class Profile(Base, IdMixin):
    level: Mapped[str] = mapped_column(String, nullable=False, default=EnglishLevel.B1)
    variant: Mapped[str] = mapped_column(
        String, nullable=False, default=EnglishVariant.BRITISH
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False, unique=True
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
    )
    words: Mapped[list["UserWord"]] = relationship(
        "UserWord",
        back_populates="profile",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    def __repr__(self) -> str:
        return f"{self.user}"
