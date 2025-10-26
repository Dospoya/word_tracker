from pydantic import BaseModel

from app.schemas.base import BaseReadModel


class Meanings(BaseModel):
    pos: str
    examples: list[str]
    synonyms: list[str]
    definition: str


class GlobalWordDB(BaseReadModel):
    word: str
    meanings: list[Meanings]
    antonyms: list[str]
    synonyms: list[str]
    count: int


class GlobalWordCreate(BaseModel):
    """Заготовки для админки"""


class GlobalWordUpdate(BaseModel):
    """Заготовки для админки"""
