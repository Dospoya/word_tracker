# from datetime import datetime

# from sqlalchemy import (
#     Column, DateTime,
#     ForeignKey, Integer,
#     UniqueConstraint
# )
# from sqlalchemy.orm import relationship

# from src.app.base import Base


# class WordProgress(Base):
#     word_id = Column(Integer, ForeignKey('word.id'), nullable=False)
#     user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
#     repetisions = Column(Integer, default=0)
#     last_reviewed = Column(DateTime, default=datetime.utcnow)
#     success_rate = Column(Integer, default=0)
#     word = relationship('Word', back_populates='progress')
#     user = relationship('User', back_populates='progress')

#     __table_args__ = [
#         UniqueConstraint('word_id', 'user_id', name='uq_user_word_progress'),
#     ]
