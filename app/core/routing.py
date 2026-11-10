from app.core.state import AgentFlowState
from app.config import settings


def should_revise(state: AgentFlowState) -> str:
    """
    Conditional routing after the Reviewer node.
    Loops back to the Coder if revision is needed and budget allows.
    """
    if (
        state["review_status"] == "NEEDS_REVISION"
        and state.get("revision_count", 0) < settings.max_revisions
    ):
        return "coder"
    return "end"
