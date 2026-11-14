"""Redis-backed rate limiter with user-aware key function."""
from slowapi import Limiter
from starlette.requests import Request

from app.config import settings


def _key_func(request: Request) -> str:
    """Prefer authenticated subject, fallback to IP."""
    auth = request.headers.get("authorization", "")
    if auth.startswith("Bearer "):
        # Use a hash of the token as key (no verification here — verification
        # is a security concern and rate limiting is best-effort).
        return f"user:{hash(auth)}"
    return f"ip:{request.client.host if request.client else 'unknown'}"


limiter = Limiter(
    key_func=_key_func,
    default_limits=[settings.rate_limit_default],
    storage_uri=settings.redis_url,
    strategy="moving-window",
)
