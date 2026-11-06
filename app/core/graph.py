from typing import Any

from app.core.state import AgentState


def build_graph() -> Any:
    """Build and return the LangGraph agent graph."""
    try:
        from langgraph.graph import StateGraph
    except ImportError:  # pragma: no cover
        raise RuntimeError("langgraph is required to build the graph")

    builder = StateGraph(AgentState)
    builder.add_node("router", lambda state: state)
    builder.add_node("researcher", lambda state: state)
    builder.add_node("coder", lambda state: state)
    builder.add_node("reviewer", lambda state: state)
    builder.set_entry_point("router")
    return builder.compile()
