"""Liveness, readiness, and Prometheus metrics endpoint."""
from fastapi import APIRouter, Depends, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

import redis

from app import __version__
from app.api.schemas import HealthResponse, ReadinessResponse
from app.config import settings
from app.db.engine import get_session

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)


@router.get("/healthz")
async def healthz() -> dict:
    """Kubernetes liveness probe."""
    return {"status": "ok"}


@router.get("/readyz", response_model=ReadinessResponse)
async def readyz(session: AsyncSession = Depends(get_session)) -> ReadinessResponse:
    """Kubernetes readiness — checks DB and Redis connectivity."""
    checks: dict[str, str] = {}

    try:
        await session.execute(text("SELECT 1"))
        checks["postgres"] = "ok"
    except Exception as exc:
        checks["postgres"] = f"error: {exc}"

    try:
        client = redis.from_url(settings.redis_url, socket_timeout=2)
        client.ping()
        checks["redis"] = "ok"
    except Exception as exc:
        checks["redis"] = f"error: {exc}"

    overall = "ok" if all(v == "ok" for v in checks.values()) else "degraded"
    return ReadinessResponse(status=overall, checks=checks)


@router.get("/metrics")
async def metrics() -> Response:
    """Prometheus scrape endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
