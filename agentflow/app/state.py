from typing import Annotated, List, Dict, Any
from typing_extensions import TypedDict


class AgentState(TypedDict):
    messages: Annotated[List[Dict[str, Any]], ...]
    step: int
    context: Dict[str, Any]
