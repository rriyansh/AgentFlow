"""Agent workflow endpoints."""
import time
import uuid

from fastapi import APIRouter, Depends, Request
from langchain_core.messages import HumanMessage
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.rate_limit import limiter
from app.api.schemas import RunRequest, RunResponse
from app.config import settings
from app.core.exceptions import WorkflowError
from app.core.graph import app as agent_app
from app.db.engine import get_session
from app.domain.repositories.workflow_runs import WorkflowRunRepository
from app.observability.metrics import AGENT_LATENCY, AGENT_RUNS
from app.security.auth import verify_api_key

router = APIRouter(prefix="/v1/agent", tags=["agent"])


@router.post(
    "/run",
    response_model=RunResponse,
    dependencies=[Depends(verify_api_key)],
    responses={401: {"description": "Invalid API key"}},
)
@limiter.limit(settings.rate_limit_run)
async def run_agent(
    request: Request,
    payload: RunRequest,
    session: AsyncSession = Depends(get_session),
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

    config = {"configurable": {"thread_id": f"{payload.user_id}:{thread_id}"}}

    try:
        final_state = await agent_app.ainvoke(initial_state, config=config)
    except Exception as exc:
        AGENT_RUNS.labels(status="error").inc()
        raise WorkflowError(
            "Workflow execution failed", details={"reason": str(exc)}
        )

    duration_ms = int((time.perf_counter() - start) * 1000)
    AGENT_RUNS.labels(status=final_state["review_status"]).inc()
    AGENT_LATENCY.observe(duration_ms / 1000)

    # Audit trail
    try:
        repo = WorkflowRunRepository(session)
        await repo.create(
            thread_id=thread_id,
            user_id=payload.user_id,
            task=payload.task,
            status=final_state["review_status"],
            revisions=final_state["revision_count"],
            duration_ms=duration_ms,
        )
    except Exception:
        pass  # audit failure must not break the request

    return RunResponse(
        thread_id=thread_id,
        status=final_state["review_status"],
        final_output=final_state["code_output"],
        revisions=final_state["revision_count"],
        token_usage=final_state.get("token_usage", {}),
    )


@router.get("/state/{thread_id}", dependencies=[Depends(verify_api_key)])
async def get_state(thread_id: str, user_id: str = "default") -> dict:
    config = {"configurable": {"thread_id": f"{user_id}:{thread_id}"}}
    snapshot = agent_app.get_state(config)
    return {"values": snapshot.values, "next": snapshot.next}
