"""FastAPI application factory with full middleware stack."""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app import __version__
from app.api.rate_limit import limiter
from app.api.routes import agent, auth, health, stream
from app.config import settings
from app.core.exceptions import AgentFlowError
from app.core.lifespan import lifespan
from app.core.middleware import RequestContextMiddleware

app = FastAPI(
    title="AgentFlow API",
    description="Enterprise multi-agent system — hardened, observable.",
    version=__version__,
    lifespan=lifespan,
)

# ── Middleware (order matters: outermost first) ──────────────
app.add_middleware(RequestContextMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    expose_headers=["x-request-id"],
)

# ── Rate limiting ────────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── Global exception handlers ────────────────────────────────
@app.exception_handler(AgentFlowError)
async def handle_agentflow_error(request: Request, exc: AgentFlowError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
                "request_id": request.headers.get("x-request-id"),
            }
        },
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "validation_error",
                "message": "Request validation failed",
                "details": exc.errors(),
                "request_id": request.headers.get("x-request-id"),
            }
        },
    )


@app.exception_handler(Exception)
async def handle_unexpected(request: Request, exc: Exception):
    # Never leak internals in production
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "internal_error",
                "message": "An internal error occurred",
                "request_id": request.headers.get("x-request-id"),
            }
        },
    )


# ── OpenTelemetry auto-instrumentation ────────────────────────
FastAPIInstrumentor.instrument_app(app)

# ── Routes ────────────────────────────────────────────────────
app.include_router(health.router)
app.include_router(agent.router)
app.include_router(stream.router)
app.include_router(auth.router)
