import pytest

from app.core.routing import should_revise


@pytest.mark.asyncio
async def test_happy_path(test_graph, sample_state):
    result = await test_graph.ainvoke(
        sample_state, config={"configurable": {"thread_id": "t1"}}
    )
    assert result["research_findings"] == "researched"
    assert result["code_output"] == "coded"


def test_routing_approved():
    assert should_revise({"review_status": "APPROVED", "revision_count": 1}) == "end"


def test_routing_needs_revision():
    assert should_revise({"review_status": "NEEDS_REVISION", "revision_count": 1}) == "coder"


def test_routing_max_reached():
    assert should_revise({"review_status": "NEEDS_REVISION", "revision_count": 10}) == "end"
