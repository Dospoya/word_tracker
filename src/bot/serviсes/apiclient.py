import logging
from types import TracebackType
from typing import Any, Optional, Type

import aiohttp

from src.app.core.config import settings

API_BOT_TOKEN = settings.api_bot_token
API_URL = settings.api_url


class APIClient:
    """Асинхронный HTTP-клиент для взаимодействия с внешним API через aiohttp.

    Используется как контекстный менеджер:
        async with APIClient() as client:
            await client.get('/example')
    """

    def __init__(
        self,
        base_url: str = API_URL,
        api_token: str = API_BOT_TOKEN,
    ) -> None:
        """Инициализация клиента."""
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
        }
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> 'APIClient':
        """Открывает aiohttp-сессию при входе в контекст."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(base_url=self.base_url)
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Закрывает aiohttp-сессию при выходе из контекста."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def get(
        self,
        path: str,
        include_auth_headers: bool = True,
        **kwargs: Any
    ) -> Any | None:
        """Выполняет GET-запрос."""
        return await self._send_request(
            'get',
            path,
            include_auth_headers=include_auth_headers,
            **kwargs
        )

    async def post(
        self,
        path: str,
        include_auth_headers: bool = True,
        **kwargs: Any
    ) -> Any | None:
        """Выполняет POST-запрос."""
        return await self._send_request(
            'post',
            path,
            include_auth_headers=include_auth_headers,
            **kwargs
        )

    async def delete(
        self,
        path: str,
        include_auth_headers: bool = True,
        **kwargs: Any
    ) -> Any | None:
        """Выполняет DELETE-запрос."""
        return await self._send_request(
            'delete',
            path,
            include_auth_headers=include_auth_headers,
            **kwargs
        )

    async def patch(
        self,
        path: str,
        include_auth_headers: bool = True,
        **kwargs: Any
    ) -> Any | None:
        """Выполняет PATCH-запрос."""
        return await self._send_request(
            'patch',
            path,
            include_auth_headers=include_auth_headers,
            **kwargs
        )

    async def _send_request(
        self,
        method: str,
        path: str,
        include_auth_headers: bool = True,
        **kwargs: Any,
    ) -> Any | None:
        """Выполняет HTTP-запрос указанного метода."""
        try:
            async with self.session.request(
                method=method,
                url=path,
                headers=self.headers if include_auth_headers else None,
                **kwargs,
            ) as response:
                # print(
                #     f'HTTP {method.upper()} {self.base_url}{path} '
                #     f'status: {response.status}, '
                #     f'response: {await response.text()}',
                # )
                response.raise_for_status()
                if response.status != 204:
                    return await response.json()
                return None
        except aiohttp.ClientError as e:
            logging.error(f'HTTP request failed: {e}')
            raise e
