from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app import __version__
from app.config import settings
from app.observability.logging import setup_logging, logger
from app.api.rate_limit import limiter
from app.api.routes import health, agent, stream
from app.core.checkpointer import close_checkpointer


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("agentflow_starting", version=__version__)
    yield
    close_checkpointer()
    logger.info("agentflow_shutdown")


app = FastAPI(
    title="AgentFlow API",
    description="Enterprise multi-agent system with fault tolerance & HITL.",
    version=__version__,
    lifespan=lifespan,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FastAPIInstrumentor.instrument_app(app)

app.include_router(health.router)
app.include_router(agent.router)
app.include_router(stream.router)
