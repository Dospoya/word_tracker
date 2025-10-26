from enum import Enum
from typing import ClassVar

from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnglishVariant(str, Enum):
    AMERICAN = "american"
    BRITISH = "british"


class EnglishLevel(str, Enum):
    A1 = "a1"
    A2 = "a2"
    B1 = "b1"
    B2 = "b2"
    C1 = "c1"
    C2 = "c2"


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class Meanings(BaseModel):
    pos: str
    examples: list[str]
    synonyms: list[str]
    definition: str


class GlobalWordDB(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)
    id: int
    word: str
    meanings: list[Meanings]
    antonyms: list[str]
    synonyms: list[str]
    count: int


class Settings(BaseSettings):
    api_url: str = "http://localhost:8000"
    api_bot_token: str = "API_TOKEN_BOT"
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )


settings = Settings()
