from enum import Enum

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship

from src.app.core.db import Base


MAX_FIELD_LEN = 128

class UserRole(str, Enum):
    USER = 'user'
    ADMIN = 'admin'

class User(SQLAlchemyBaseUserTable[int], Base):
    tg_id = Column(BigInteger, unique=True)
    first_name = Column(String(MAX_FIELD_LEN), nullable=False)
    role = Column(String, nullable=False, default=UserRole.ADMIN)
    profile = relationship(
        'Profile',
        back_populates='user',
        uselist=False,
        cascade='delete',
    )
    # progress = relationship('WordProgress', back_populates='user')

    def __repr__(self) -> str:
        return (
            f'{self.first_name}. '
            f'{self.id}'
        )
