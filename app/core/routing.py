from app.core.state import AgentState


def route(state: AgentState) -> str:
    query = (state.query or "").lower()
    if "code" in query:
        return "coder"
    if "review" in query:
        return "reviewer"
    return "researcher"
