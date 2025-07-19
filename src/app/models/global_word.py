from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.app.core.base import Base


MAX_WORD_LEN = 128


class GlobalWord(Base):
    word = Column(String(MAX_WORD_LEN), nullable=False, unique=True)
    definition = Column(String)
    transcription = Column(String, nullable=False)
    category = Column(String)
    synonyms = Column(String)
    example = Column(String)
    translation = Column(String)
    user_words = relationship(
        'UserWord',
        back_populates='global_word',
    )

    def __repr__(self) -> str:
        return f'{self.word}.'
