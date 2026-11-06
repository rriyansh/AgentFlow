from datetime import datetime, timedelta, timezone
from typing import Any

import jwt


def create_access_token(
    subject: str, secret_key: str, expires_minutes: int = 30
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload: dict[str, Any] = {"sub": subject, "exp": expire}
    return jwt.encode(payload, secret_key, algorithm="HS256")


def decode_access_token(token: str, secret_key: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None
