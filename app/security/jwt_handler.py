"""JWT issue / verify / revoke with JTI tracking in Redis."""
import secrets
import time
from typing import Any

import jwt
import redis

from app.config import settings

_redis: redis.Redis | None = None


def _client() -> redis.Redis:
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def issue_access_token(subject: str, *, scopes: list[str] | None = None) -> tuple[str, int]:
    """Returns (token, ttl_seconds)."""
    ttl = settings.jwt_access_ttl_minutes * 60
    jti = secrets.token_urlsafe(16)
    now = int(time.time())
    payload = {
        "sub": subject,
        "scopes": scopes or [],
        "iat": now,
        "exp": now + ttl,
        "jti": jti,
        "type": "access",
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token, ttl


def issue_refresh_token(subject: str) -> tuple[str, int]:
    ttl = settings.jwt_refresh_ttl_days * 86400
    jti = secrets.token_urlsafe(16)
    now = int(time.time())
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + ttl,
        "jti": jti,
        "type": "refresh",
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token, ttl


def verify_token(token: str, *, expected_type: str = "access") -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

    if payload.get("type") != expected_type:
        raise ValueError(f"Expected {expected_type} token")

    jti = payload.get("jti")
    if jti and _client().exists(f"jwt:revoked:{jti}"):
        raise ValueError("Token revoked")

    return payload


def revoke_token(payload: dict[str, Any]) -> None:
    jti = payload.get("jti")
    exp = payload.get("exp", 0)
    if not jti:
        return
    ttl = max(1, int(exp - time.time()))
    _client().setex(f"jwt:revoked:{jti}", ttl, "1")
