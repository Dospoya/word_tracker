from fastapi_users import schemas
from pydantic import BaseModel, PositiveInt, field_validator, Field

from app.models.user import UserRole
from .validators import validate_non_empty


class UserBaseMixin(BaseModel):
    first_name: str
    tg_id: PositiveInt
    role: UserRole = Field(default=UserRole.ADMIN)

    _validate_first_name = field_validator('first_name')(validate_non_empty)
    _validate_last_name = field_validator('last_name')(validate_non_empty)


class UserUpdateMixin(BaseModel):
    first_name: str | None
    tg_id: PositiveInt | None
    role: UserRole | None

    _validate_first_name = field_validator('first_name')(
        lambda v: validate_non_empty(v, allow_none=True))
    _validate_last_name = field_validator('last_name')(
        lambda v: validate_non_empty(v, allow_none=True))


class UserCreate(UserBaseMixin, schemas.BaseUserCreate):
    pass


class UserUpdate(UserUpdateMixin, schemas.BaseUserUpdate):
    pass


class UserDB(UserBaseMixin, schemas.BaseUser[int]):
    pass
