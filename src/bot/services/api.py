import logging
from datetime import datetime
from typing import Any

from aiohttp import ClientResponseError

from bot.services.bot_requests import (
    add_word_to_user,
    create_profile,
    create_user,
    get_global_word,
    get_user_by_tg_id,
    get_user_words,
)
from contracts.shared.contracts import UserRole


async def full_user_registration(
    first_name: str,
    tg_id: int,
    level: str,
    variant: str,
):
    now = datetime.now()
    timestamp = str(int(now.timestamp()))[-6:]
    email = f"user{timestamp}@example.com"
    password = f"p@ssW0rD!{timestamp}"
    try:
        user = await create_user(
            first_name=first_name,
            tg_id=tg_id,
            email=email,
            password=password,
            role=UserRole.USER,
        )
        user_id = user.get("id")
    except Exception as e:
        logging.info(f"Ошибка создания пользователя c tg_id: {tg_id}: {e}")
        raise e
    try:
        _ = await create_profile(
            user_id=user_id,
            level=level,
            variant=variant,
        )
        return True
    except Exception as e:
        logging.info(f"Ошибка создания профиля c tg_id: {tg_id}: {e}")
        raise e


async def check_user_role(tg_id: int):
    try:
        user = await get_user_by_tg_id(tg_id)
        return user.get("role")
    except ClientResponseError as e:
        if e.status == 404:
            return None
        logging.error(f"Ошибка получения роли пользователя c tg_id: {tg_id}: {e}")
        raise
    except Exception as e:
        logging.error(
            f"Неизвестная ошибка при получении роли пользователя {tg_id}: {e}"
        )
        raise


async def get_word(word: str):
    try:
        return await get_global_word(word)
    except ClientResponseError as e:
        if e.status == 404:
            return None
        logging.error(f"Ошибка получения слова {word}: {e}")
        raise
    except Exception as e:
        logging.error(f"Неизвестная ошибка при получении слова {word}: {e}")
        raise


async def add_word(word: str, tg_id: int):
    try:
        return await add_word_to_user(word, tg_id)
    except ClientResponseError as e:
        if e.status == 404:
            return None
        logging.error(f"Ошибка добавления слова {word}: {e}")
        raise
    except Exception as e:
        logging.error(f"Неизвестная ошибка при добавлении слова {word}: {e}")
        raise


async def get_words_by_tg_id(tg_id: int) -> list[dict[str, Any]]:
    return await get_user_words(tg_id)
