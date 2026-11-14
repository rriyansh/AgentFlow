"""Server-Sent Events streaming endpoint."""
import json

from fastapi import APIRouter, Depends
from langchain_core.messages import HumanMessage
from sse_starlette.sse import EventSourceResponse

from app.api.schemas import RunRequest
from app.core.graph import app as agent_app
from app.security.auth import verify_api_key

router = APIRouter(prefix="/v1/agent", tags=["stream"])


@router.post("/stream", dependencies=[Depends(verify_api_key)])
async def stream_agent(payload: RunRequest):
    thread_id = payload.thread_id or "stream-session"
    config = {"configurable": {"thread_id": f"{payload.user_id}:{thread_id}"}}

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
            if name not in ("researcher", "coder", "reviewer"):
                continue
            if kind == "on_chain_start":
                yield {"event": "node_start", "data": json.dumps({"node": name})}
            elif kind == "on_chain_end":
                yield {"event": "node_end", "data": json.dumps({"node": name})}

    return EventSourceResponse(event_generator())
