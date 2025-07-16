from pydantic import BaseModel, ConfigDict, field_validator

from .base import BaseReadModel
from .validators import validate_non_empty

class ProfileBase(BaseModel):
    level: str
    variant: str
    user_id: int

    _validate_level = field_validator('level')(validate_non_empty)
    _validate_variant = field_validator('variant')(validate_non_empty)


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    level: str | None
    variant: str | None

    _validate_level = field_validator('level')(
        lambda v: validate_non_empty(v, allow_none=True))
    _validate_variant = field_validator('variant')(
        lambda v: validate_non_empty(v, allow_none=True))


class ProfileDB(BaseReadModel, ProfileBase):
    pass
