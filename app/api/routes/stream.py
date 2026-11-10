import json
from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse
from langchain_core.messages import HumanMessage
from app.api.schemas import RunRequest
from app.security.auth import verify_api_key
from app.core.graph import app as agent_app

router = APIRouter(prefix="/v1/agent", tags=["stream"])


@router.post("/stream")
async def stream_agent(
    payload: RunRequest, _: str = Depends(verify_api_key)
):
    """Stream node-level events via Server-Sent Events."""
    thread_id = payload.thread_id or "stream-session"
    config = {
        "configurable": {"thread_id": f"{payload.user_id}:{thread_id}"}
    }

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

    async def event_generator():
        async for event in agent_app.astream_events(
            initial_state, config=config, version="v2"
        ):
            kind = event["event"]
            name = event.get("name", "")
            if kind == "on_chain_start" and name in (
                "researcher", "coder", "reviewer"
            ):
                yield {
                    "event": "node_start",
                    "data": json.dumps({"node": name}),
                }
            elif kind == "on_chain_end" and name in (
                "researcher", "coder", "reviewer"
            ):
                yield {
                    "event": "node_end",
                    "data": json.dumps({"node": name}),
                }

    return EventSourceResponse(event_generator())
