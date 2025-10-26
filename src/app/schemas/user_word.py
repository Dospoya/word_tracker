from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.models.user_word import WordStatus
from app.schemas.base import BaseReadModel
from app.schemas.global_word import GlobalWordDB
from app.schemas.validators import validate_english_word

MAX_WORD_LEN = 128
MIN_WORD_LEN = 1


class UserWordBase(BaseModel):
    status: WordStatus
    added_at: datetime


class UserWordCreate(BaseModel):
    word: str = Field(..., min_length=MIN_WORD_LEN, max_length=MAX_WORD_LEN)

    _validate_word = field_validator("word")(validate_english_word)


class UserWordCreateResponse(BaseModel):
    created: bool


class UserWordUpdate(BaseModel):
    status: WordStatus | None = None


class UserWordItem(UserWordBase, BaseReadModel):
    word: str
    meanings: list[str] | None


class UserWordDetail(UserWordBase, BaseReadModel):
    global_word: GlobalWordDB
