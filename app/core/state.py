from typing import Any, Optional

from pydantic import BaseModel


class AgentState(BaseModel):
    query: str
    route: Optional[str] = None
    result: Optional[Any] = None
    context: dict[str, Any] = {}
    error: Optional[str] = None
