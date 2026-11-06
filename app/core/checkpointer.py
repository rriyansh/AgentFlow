from typing import Any


class BaseCheckpointer:
    """Base checkpointer for persisting graph state."""

    async def get(self, key: str) -> Any | None:
        raise NotImplementedError

    async def put(self, key: str, value: Any) -> None:
        raise NotImplementedError
