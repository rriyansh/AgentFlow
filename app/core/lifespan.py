"""Application lifespan: startup and graceful shutdown orchestration."""
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app import __version__
from app.config import settings
from app.core.checkpointer import close_checkpointer
from app.db.engine import close_engine
from app.observability.logging import logger, setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup_logging()
    logger.info(
        "agentflow_starting",
        version=__version__,
        environment=settings.environment,
    )
    try:
        yield
    finally:
        logger.info("agentflow_shutdown_start")
        close_checkpointer()
        await close_engine()
        logger.info("agentflow_shutdown_complete")
