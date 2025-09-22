from typing import List

from pydantic import BaseModel
from pydantic.types import PositiveInt

from .base import BaseReadModel


class Meanings(BaseModel):
    pos: str
    examples: List[str]
    synonyms: List[str]
    definition: str


class GlobalWordDB(BaseReadModel):
    word: str
    meanings: List[Meanings]
    antonyms: List[str]
    synonyms: List[str]
    count: PositiveInt


class GlobalWordCreate(BaseModel):
    """Заготовки для админки"""


class GlobalWordUpdate(BaseModel):
    """Заготовки для админки"""
