from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from src.app.core.base import Base


MAX_WORD_LEN = 128


class GlobalWord(Base):
    word = Column(String(MAX_WORD_LEN), nullable=False, unique=True)
    meanings = Column(JSONB, default=list, nullable=False)
    antonyms = Column(JSONB, default=list, nullable=False)
    synonyms = Column(JSONB, default=list, nullable=False)
    count = Column(
        Integer,
        default=0,
        nullable=False,
        doc='Количество добавлений слова'
    )
    user_words = relationship(
        'UserWord',
        back_populates='global_word',
    )

    def __repr__(self) -> str:
        return f'{self.word}.'
