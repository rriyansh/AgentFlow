# SlowAPI + Redisfrom slowapi import Limiter
from slowapi.util import get_remote_address
from app.config import settings

# Redis storage ensures distributed rate limiting across all workers
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.rate_limit_default],
    storage_uri=settings.redis_url,
    strategy="moving-window",
)
