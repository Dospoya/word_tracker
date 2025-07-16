from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
    field_validator)

from .base import BaseReadModel
from .validators import (
    validate_non_empty,
    validate_english_word,
    validate_russian_word)


MAX_WORD_LEN = 128
MIN_WORD_LEN = 1


class WordBase(BaseModel):
    word: str = Field(..., min_length=MIN_WORD_LEN, max_length=MAX_WORD_LEN)
    synonyms: str
    example: str
    translation: str
    profile_id: PositiveInt

    _validate_word = field_validator('word')(validate_english_word)
    _validate_synonyms = field_validator('synonyms')(validate_non_empty)
    _validate_example = field_validator('example')(validate_non_empty)
    _validate_translation = field_validator('translation')(validate_russian_word)

class WordCreate(WordBase):
    pass


class WordUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    word: str | None
    synonyms: str | None
    example: str | None
    translation: str | None
    profile_id: PositiveInt | None

    _validate_word = field_validator('word')(
        lambda v: validate_english_word(v, allow_none=True))
    _validate_synonyms = field_validator('synonyms')(
        lambda v: validate_non_empty(v, allow_none=True))
    _validate_example = field_validator('example')(
        lambda v: validate_non_empty(v, allow_none=True))
    _validate_translation = field_validator('translation')(
        lambda v: validate_russian_word(v, allow_none=True))

class WordDB(BaseReadModel, WordBase):
    pass
