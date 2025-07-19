from .apiclient import APIClient


USER_BASE_PATH = '/bot/users'
USER_DETAIL_PATH = '/bot/users/{tg_id}'
PROFILE_CREATE_PATH = '/bot/users/profile'


async def create_user(
    **kwargs,
):
    payload = {k: v for k, v in kwargs.items() if v is not None}
    async with APIClient() as client:
        return await client.post(
            path=USER_BASE_PATH,
            json=payload,
        )


async def create_profile(
    **kwargs,
):
    payload = {k: v for k, v in kwargs.items() if v is not None}
    async with APIClient() as client:
        return await client.post(
            path=PROFILE_CREATE_PATH,
            json=payload,
        )


async def get_user_by_tg_id(
    tg_id: int,
):
    async with APIClient() as client:
        return await client.get(
            path=USER_DETAIL_PATH.format(tg_id=tg_id)
        )
