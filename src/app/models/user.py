from enum import Enum
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.profile import Profile

MAX_FIELD_LEN = 128


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String(MAX_FIELD_LEN), nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default=UserRole.ADMIN)
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="delete",
    )

    def __repr__(self) -> str:
        return f"{self.first_name}. {self.id}"
