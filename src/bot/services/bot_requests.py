from typing import Any

from bot.services.apiclient import APIClient
from contracts.shared.contracts import UserRole

USER_BASE_PATH = "/bot/users"
USER_DETAIL_PATH = "/bot/users/{tg_id}"
USER_WORDS_PATH = "/bot/users/{tg_id}/words"
USER_ADD_WORD_PATH = "/bot/users/{tg_id}/add_word"
PROFILE_CREATE_PATH = "/bot/users/profile"
GET_WORD_PATH = "/bot/words/{word}"


async def create_user(
    tg_id: int,
    first_name: str,
    email: str,
    password: str,
    role: UserRole,
):
    payload = dict(
        tg_id=tg_id, first_name=first_name, email=email, password=password, role=role
    )
    async with APIClient() as client:
        return await client.post(
            path=USER_BASE_PATH,
            json=payload,
        )


async def create_profile(
    user_id: int,
    variant: str,
    level: str,
):
    payload = dict(user_id=user_id, variant=variant, level=level)
    async with APIClient() as client:
        return await client.post(
            path=PROFILE_CREATE_PATH,
            json=payload,
        )


async def get_user_by_tg_id(
    tg_id: int,
):
    async with APIClient() as client:
        return await client.get(path=USER_DETAIL_PATH.format(tg_id=tg_id))


async def get_global_word(word: str):
    async with APIClient() as client:
        return await client.get(path=GET_WORD_PATH.format(word=word))


async def add_word_to_user(
    word: str,
    tg_id: int,
):
    async with APIClient() as client:
        return await client.post(
            path=USER_ADD_WORD_PATH.format(tg_id=tg_id),
            json={"word": word},
        )


async def get_user_words(tg_id: int) -> list[dict[str, Any]]:
    async with APIClient() as client:
        return await client.get(path=USER_WORDS_PATH.format(tg_id=tg_id))
