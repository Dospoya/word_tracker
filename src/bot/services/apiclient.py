import logging
from types import TracebackType
from typing import Any

import aiohttp

from contracts.shared.contracts import settings

JSONType = dict[str, Any] | list[Any] | None


class APIClient:
    """Асинхронный HTTP-клиент для взаимодействия с внешним API через aiohttp.

    Используется как контекстный менеджер:
        async with APIClient() as client:
            await client.get('/example')
    """

    def __init__(
        self,
        base_url: str = settings.api_url,
        api_token: str = settings.api_bot_token,
    ) -> None:
        """Инициализация клиента."""
        self.base_url: str = base_url
        self.headers: dict[str, str] = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "APIClient":
        """Открывает aiohttp-сессию при входе в контекст."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(base_url=self.base_url)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Закрывает aiohttp-сессию при выходе из контекста."""
        if self.session and not self.session.closed:
            await (
                self.session.close()
            )  # (basedpyright: ignore[reportGeneralTypeIssues])

    async def get(
        self, path: str, include_auth_headers: bool = True, **kwargs: dict[str, Any]
    ) -> JSONType:
        """Выполняет GET-запрос."""
        return await self._send_request(
            "get", path, include_auth_headers=include_auth_headers, **kwargs
        )

    async def post(
        self, path: str, include_auth_headers: bool = True, **kwargs: dict[str, Any]
    ) -> JSONType:
        """Выполняет POST-запрос."""
        return await self._send_request(
            "post", path, include_auth_headers=include_auth_headers, **kwargs
        )

    async def delete(
        self, path: str, include_auth_headers: bool = True, **kwargs: dict[str, Any]
    ) -> JSONType:
        """Выполняет DELETE-запрос."""
        return await self._send_request(
            "delete", path, include_auth_headers=include_auth_headers, **kwargs
        )

    async def patch(
        self, path: str, include_auth_headers: bool = True, **kwargs: dict[str, Any]
    ) -> JSONType:
        """Выполняет PATCH-запрос."""
        return await self._send_request(
            "patch", path, include_auth_headers=include_auth_headers, **kwargs
        )

    async def _send_request(
        self,
        method: str,
        path: str,
        include_auth_headers: bool = True,
        **kwargs: dict[str, Any],
    ) -> JSONType:
        """Выполняет HTTP-запрос указанного метода."""
        try:
            async with self.session.request(
                method=method,
                url=path,
                headers=self.headers if include_auth_headers else None,
                **kwargs,
            ) as response:
                response.raise_for_status()
                if response.status != 204:
                    return await response.json()
                return None
        except aiohttp.ClientError as e:
            logging.error(f"HTTP request failed: {e}")
            raise e
