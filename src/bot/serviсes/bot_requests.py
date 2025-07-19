from .apiclient import APIClient


USER_REGISTER_PATH = '/bot/users'
PROFILE_CREATE_PATH = '/bot/users/profile'


async def create_user(
    **kwargs,
):
    payload = {k: v for k, v in kwargs.items() if v is not None}
    async with APIClient() as client:
        return await client.post(
            path=USER_REGISTER_PATH,
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
