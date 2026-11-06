from app.core.graph import build_graph
from app.core.state import AgentState


def test_graph_builds() -> None:
    graph = build_graph()
    assert graph is not None


def test_graph_invocation() -> None:
    graph = build_graph()
    state = AgentState(query="test query")
    result = graph.invoke(state)
    assert result is not None
