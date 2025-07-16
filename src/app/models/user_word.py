from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from src.app.core.db import Base


MAX_WORD_LEN = 128


class WordStatus(str, Enum):
    NEW = 'new'
    LEARNING = 'learning'
    MASTERED = 'mastered'


class UserWord(Base):
    word_id = Column(Integer, ForeignKey('global_word.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    status = Column(String, default=WordStatus.NEW)
    added_at = Column(DateTime, default=datetime.utcnow)
    global_word = relationship('GlobalWord', back_populates='user_words', lazy='joined')
    profile = relationship('Profile', back_populates='words')
    # progress = relationship(
    #     'WordProgress',
    #     back_populates='word',
    #     cascade='all, delete-orphan'
    # )
    __table_args__ = (
        UniqueConstraint('word_id', 'user_id', name='unique_word_user'),
    )

    def __repr__(self) -> str:
        return f'{self.global_word.word}'
