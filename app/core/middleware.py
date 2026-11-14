"""Request ID + body size + HTTP metrics middleware."""
import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp

from app.config import settings
from app.observability.metrics import HTTP_REQUEST_DURATION, HTTP_REQUESTS

logger = structlog.get_logger()


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Attaches a request_id, enforces body size, logs request context."""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())

        # Enforce body size limit (Content-Length only — streaming limits
        # should be configured at the reverse proxy level for real safety).
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > settings.max_request_bytes:
            return JSONResponse(
                status_code=413,
                content={
                    "error": {
                        "code": "payload_too_large",
                        "message": f"Request exceeds {settings.max_request_bytes} bytes",
                        "request_id": request_id,
                    }
                },
            )

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        start = time.perf_counter()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers["x-request-id"] = request_id
            return response
        finally:
            duration = time.perf_counter() - start
            HTTP_REQUESTS.labels(
                method=request.method,
                path=request.url.path,
                status=str(status_code),
            ).inc()
            HTTP_REQUEST_DURATION.labels(method=request.method).observe(duration)
            logger.info(
                "http_request",
                method=request.method,
                path=request.url.path,
                status=status_code,
                duration_ms=round(duration * 1000, 2),
            )
