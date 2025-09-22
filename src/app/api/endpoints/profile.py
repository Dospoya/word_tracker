from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.profile import profile_crud
from src.app.models import Profile

router = APIRouter()

# @router.get(
#     '',
#     response_model=Profile,
#     dependencies=[Depends(...)]
# )
