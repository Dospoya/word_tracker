from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.app.core.base import Base


class EnglishVariant(str, Enum):
    AMERICAN = 'american'
    BRITISH = 'british'


class EnglishLevel(str, Enum):
    A1 = 'a1'
    A2 = 'a2'
    B1 = 'b1'
    B2 = 'b2'
    C1 = 'c1'
    C2 = 'c2'


class Profile(Base):
    level = Column(String, nullable=False, default=EnglishLevel.B1)
    variant = Column(String, nullable=False, default=EnglishVariant.BRITISH)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, unique=True)
    user = relationship(
        'User',
        back_populates='profile',
    )
    # words = relationship(
    #     'UserWord',
    #     back_populates='profile',
    #     cascade='all, delete-orphan',
    #     single_parent=True
    # )

    def __repr__(self) ->str:
        return f'{self.user}'
