"""PostgresSaver singleton with connection pooling."""
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool

from app.config import settings

_pool: ConnectionPool | None = None
_checkpointer: PostgresSaver | None = None


def get_checkpointer() -> PostgresSaver:
    global _pool, _checkpointer
    if _checkpointer is None:
        _pool = ConnectionPool(
            conninfo=settings.postgres_uri,
            min_size=settings.db_pool_min_size,
            max_size=settings.db_pool_max_size,
            timeout=30,
            open=True,
        )
        _checkpointer = PostgresSaver(_pool)
        _checkpointer.setup()
    return _checkpointer


def close_checkpointer() -> None:
    global _pool, _checkpointer
    if _pool is not None:
        _pool.close()
    _pool = None
    _checkpointer = None
