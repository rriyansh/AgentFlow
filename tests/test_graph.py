import pytest
from app.core.routing import should_revise


@pytest.mark.asyncio
async def test_graph_happy_path(test_graph, sample_state):
    result = await test_graph.ainvoke(
        sample_state,
        config={"configurable": {"thread_id": "test-1"}},
    )
    assert result["research_findings"] == "researched"
    assert result["code_output"] == "coded"


def test_should_revise_approved():
    state = {"review_status": "APPROVED", "revision_count": 1}
    assert should_revise(state) == "end"


def test_should_revise_needs_revision():
    state = {"review_status": "NEEDS_REVISION", "revision_count": 1}
    assert should_revise(state) == "coder"


def test_should_revise_max_reached():
    state = {"review_status": "NEEDS_REVISION", "revision_count": 10}
    assert should_revise(state) == "end"
