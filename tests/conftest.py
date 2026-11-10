import pytest
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from app.core.state import AgentFlowState


@pytest.fixture
def sample_state() -> AgentFlowState:
    return {
        "messages": [],
        "research_findings": "",
        "code_output": "",
        "review_status": "",
        "review_feedback": "",
        "revision_count": 0,
        "thread_id": "test-thread",
        "user_id": "test-user",
        "token_usage": {},
    }


@pytest.fixture
def test_graph():
    """Minimal graph with MemorySaver for fast, isolated tests."""

    def node_a(state: dict) -> dict:
        return {"research_findings": "researched"}

    def node_b(state: dict) -> dict:
        return {"code_output": "coded"}

    workflow = StateGraph(AgentFlowState)
    workflow.add_node("a", node_a)
    workflow.add_node("b", node_b)
    workflow.set_entry_point("a")
    workflow.add_edge("a", "b")
    workflow.add_edge("b", END)
    return workflow.compile(checkpointer=MemorySaver())
