from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import settings

bearer_scheme = HTTPBearer()

async def verify_bot_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> None:
    if credentials.credentials != settings.api_bot_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid bot token",
        )
