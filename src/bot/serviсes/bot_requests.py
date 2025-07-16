from .apiclient import APIClient


USER_REGISTER_PATH = '/bot/users'


async def register_user(
    **kwargs,
):
    payload = {k: v for k, v in kwargs.items() if v is not None}
    async with APIClient() as client:
        return await client.post(
            path=USER_REGISTER_PATH,
            payload=payload,
        )
