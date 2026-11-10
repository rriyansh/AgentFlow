import uuid
import time
from fastapi import APIRouter, Depends, HTTPException, Request
from langchain_core.messages import HumanMessage
from app.api.schemas import RunRequest, RunResponse
from app.security.auth import verify_api_key
from app.api.rate_limit import limiter
from app.core.graph import app as agent_app
from app.observability.metrics import AGENT_RUNS, AGENT_LATENCY

router = APIRouter(prefix="/v1/agent", tags=["agent"])


@router.post("/run", response_model=RunResponse)
@limiter.limit("10/minute")
async def run_agent(
    request: Request,
    payload: RunRequest,
    _: str = Depends(verify_api_key),
) -> RunResponse:
    thread_id = payload.thread_id or str(uuid.uuid4())
    start = time.perf_counter()

    initial_state = {
        "messages": [HumanMessage(content=payload.task)],
        "research_findings": "",
        "code_output": "",
        "review_status": "",
        "review_feedback": "",
        "revision_count": 0,
        "thread_id": thread_id,
        "user_id": payload.user_id,
        "token_usage": {},
    }

    # Multi-tenant isolation: thread scoped to user
    config = {"configurable": {"thread_id": f"{payload.user_id}:{thread_id}"}}

    try:
        final_state = await agent_app.ainvoke(initial_state, config=config)
        AGENT_RUNS.labels(status=final_state["review_status"]).inc()
        AGENT_LATENCY.observe(time.perf_counter() - start)
        return RunResponse(
            thread_id=thread_id,
            status=final_state["review_status"],
            final_output=final_state["code_output"],
            revisions=final_state["revision_count"],
            token_usage=final_state.get("token_usage", {}),
        )
    except Exception as exc:
        AGENT_RUNS.labels(status="error").inc()
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/state/{thread_id}")
async def get_state(
    thread_id: str,
    user_id: str = "default",
    _: str = Depends(verify_api_key),
) -> dict:
    config = {"configurable": {"thread_id": f"{user_id}:{thread_id}"}}
    snapshot = agent_app.get_state(config)
    return {"values": snapshot.values, "next": snapshot.next}
