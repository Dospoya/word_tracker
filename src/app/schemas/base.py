from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class BaseReadModel(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)
    id: int
