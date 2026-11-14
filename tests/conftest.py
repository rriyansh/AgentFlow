"""Test fixtures — MemorySaver graph + FastAPI test client."""
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from app.api.dependencies import get_workflow_repo
from app.config import settings
from app.core.state import AgentFlowState
from app.main import app


@pytest.fixture
def sample_state() -> AgentFlowState:
    return {
        "messages": [],
        "research_findings": "",
        "code_output": "",
        "review_status": "",
        "review_feedback": "",
        "revision_count": 0,
        "thread_id": "test",
        "user_id": "test",
        "token_usage": {},
    }


@pytest.fixture
def test_graph():
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


class _StubRepo:
    async def create(self, **kwargs):
        return None


@pytest.fixture
async def client():
    async def _override_repo():
        return _StubRepo()

    app.dependency_overrides[get_workflow_repo] = _override_repo
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers={"x-api-key": settings.agentflow_api_key},
    ) as c:
        yield c
    app.dependency_overrides.clear()
