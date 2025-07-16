import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Добавление суперюзера при старте приложения."""
    await create_first_superuser()
    logger.info("Суперпользователь уже существует или успешно создан.")
    yield


app = FastAPI(title=settings.app_title, lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=settings.secret)

app.include_router(main_router)
