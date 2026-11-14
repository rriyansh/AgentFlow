"""Async SQLAlchemy engine and session factory."""
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def _to_async_uri(uri: str) -> str:
    """Convert postgresql:// to postgresql+asyncpg:// for SQLAlchemy async."""
    if uri.startswith("postgresql+asyncpg://"):
        return uri
    return uri.replace("postgresql://", "postgresql+asyncpg://", 1)


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            _to_async_uri(settings.postgres_uri),
            pool_size=settings.db_pool_min_size,
            max_overflow=settings.db_pool_max_size - settings.db_pool_min_size,
            pool_pre_ping=True,
            echo=False,
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            get_engine(), expire_on_commit=False, class_=AsyncSession
        )
    return _session_factory


async def get_session() -> AsyncSession:
    """FastAPI dependency: yields an AsyncSession and ensures cleanup."""
    async with get_session_factory()() as session:
        yield session


async def close_engine() -> None:
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
    _engine = None
    _session_factory = None
