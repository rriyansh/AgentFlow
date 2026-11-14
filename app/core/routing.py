"""Conditional edge logic."""
from app.config import settings
from app.core.state import AgentFlowState


def should_revise(state: AgentFlowState) -> str:
    if (
        state["review_status"] == "NEEDS_REVISION"
        and state.get("revision_count", 0) < settings.max_revisions
    ):
        return "coder"
    return "end"
