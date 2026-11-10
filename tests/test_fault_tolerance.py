import pytest
from langgraph.graph import StateGraph, END
from langgraph.types import RetryPolicy


@pytest.mark.asyncio
async def test_retry_on_transient_failure():
    """Node fails twice then succeeds; retry policy should recover."""
    call_count = {"n": 0}

    def flaky_node(state):
        call_count["n"] += 1
        if call_count["n"] < 3:
            raise ConnectionError("Transient network error")
        return {"code_output": "success"}

    workflow = StateGraph(dict)
    workflow.add_node(
        "flaky",
        flaky_node,
        retry_policy=RetryPolicy(
            max_attempts=3, initial_interval=0.1
        ),
    )
    workflow.set_entry_point("flaky")
    workflow.add_edge("flaky", END)
    graph = workflow.compile()

    result = await graph.ainvoke({"code_output": ""})
    assert result["code_output"] == "success"
    assert call_count["n"] == 3


@pytest.mark.asyncio
async def test_timeout_enforcement():
    """Node exceeding timeout should raise NodeTimeoutError."""
    import time
    from langgraph.types import TimeoutPolicy

    def slow_node(state):
        time.sleep(5)
        return {"code_output": "done"}

    workflow = StateGraph(dict)
    workflow.add_node(
        "slow",
        slow_node,
        timeout=TimeoutPolicy(run_timeout=0.5),
    )
    workflow.set_entry_point("slow")
    workflow.add_edge("slow", END)
    graph = workflow.compile()

    with pytest.raises(Exception):
        await graph.ainvoke({"code_output": ""})
