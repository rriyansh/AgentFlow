from typing import Any, Optional

from fastapi import Depends, HTTPException, status

from app.config import settings


async def get_settings() -> Any:
    return settings


async def verify_token(token: Optional[str] = Depends()) -> bool:
    if not token or token != settings.secret_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return True
