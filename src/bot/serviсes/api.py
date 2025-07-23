import logging
from datetime import datetime

from aiohttp import ClientResponseError

from src.app.models.user import UserRole
from .bot_requests import (
    create_profile,
    create_user,
    get_user_by_tg_id,
)


async def full_user_registration(
    first_name: str,
    tg_id: int,
    level: str,
    variant: str,
):
    now = datetime.now()
    timestamp = str(int(now.timestamp()))[-6:]
    email = f'user{timestamp}@example.com'
    password = f'p@ssW0rD!{timestamp}'
    try:
        user = await create_user(
            first_name=first_name,
            tg_id=tg_id,
            email=email,
            password=password,
            role=UserRole.USER,
        )
        user_id = user.get('id')
    except Exception as e:
        logging.info(f'Ошибка создания пользователя c tg_id: {tg_id}: {e}')
        raise e
    try:
        await create_profile(
            user_id=user_id,
            level=level,
            variant=variant,
        )
        return True
    except Exception as e:
        logging.info(f'Ошибка создания профиля c tg_id: {tg_id}: {e}')
        raise e


async def check_user_role(tg_id: int):
    try:
        user = await get_user_by_tg_id(tg_id)
        return user.get('role')
    except ClientResponseError as e:
        if e.status == 404:
            return None
        logging.error(f'Ошибка получения роли пользователя c tg_id: {tg_id}: {e}')
        raise
    except Exception as e:
        logging.error(f'Неизвестная ошибка при получении роли пользователя {tg_id}: {e}')
        raise
