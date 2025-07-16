from pydantic import BaseModel, ConfigDict


class BaseReadModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
