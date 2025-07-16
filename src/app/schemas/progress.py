# from datetime import datetime

# from pydantic import BaseModel, Field, PositiveInt

# from .base import BaseReadModel


# TIME_EXAMPLE = '2010-10-10T00:00'


# class WordProgressBase(BaseModel):
#     word_id: PositiveInt
#     user_id: PositiveInt
#     repetisions: PositiveInt
#     last_reviewed: datetime = Field(..., examples=[TIME_EXAMPLE])
#     success_rate: PositiveInt


# class WordProgressCreate(WordProgressBase):
#     pass


# class WordProgressUpdate(BaseModel):
#     word_id: PositiveInt | None
#     user_id: PositiveInt | None
#     repetisions: PositiveInt | None
#     last_reviewed: datetime = Field(None, examples=[TIME_EXAMPLE])
#     success_rate: PositiveInt | None


# class WordProgressDB(BaseReadModel, WordProgressBase):
#     pass
