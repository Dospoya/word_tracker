from typing import List

from pydantic import BaseModel
from pydantic.types import PositiveInt

from .base import BaseReadModel
from src.app.models import WordStatus


class UserWordBase(BaseReadModel):
    ...
