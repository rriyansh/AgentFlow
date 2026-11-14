import time

import pytest
from langgraph.graph import END, StateGraph
from langgraph.types import RetryPolicy, TimeoutPolicy


@pytest.mark.asyncio
async def test_retry_recovers_transient_failure():
    count = {"n": 0}

    def flaky(state):
        count["n"] += 1
        if count["n"] < 3:
            raise ConnectionError("transient")
        return {"ok": True}

    wf = StateGraph(dict)
    wf.add_node("f", flaky, retry_policy=RetryPolicy(max_attempts=3, initial_interval=0.05))
    wf.set_entry_point("f")
    wf.add_edge("f", END)
    g = wf.compile()
    result = await g.ainvoke({})
    assert result["ok"] is True
    assert count["n"] == 3


@pytest.mark.asyncio
async def test_timeout_enforced():
    def slow(state):
        time.sleep(3)
        return {"ok": True}

    wf = StateGraph(dict)
    wf.add_node("s", slow, timeout=TimeoutPolicy(run_timeout=0.5))
    wf.set_entry_point("s")
    wf.add_edge("s", END)
    g = wf.compile()
    with pytest.raises(Exception):
        await g.ainvoke({})
