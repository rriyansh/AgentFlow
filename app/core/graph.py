from langgraph.graph import StateGraph, END
from app.core.state import AgentFlowState
from app.core.checkpointer import get_checkpointer
from app.core.routing import should_revise
from app.core.fault_tolerance import (
    get_retry_policy,
    get_node_timeout,
    handle_node_failure,
)
from app.agents.researcher import researcher_node
from app.agents.coder import coder_node
from app.agents.reviewer import reviewer_node


def build_graph() -> StateGraph:
    workflow = StateGraph(AgentFlowState)

    # Each node gets retry policy, timeout, and fallback error handler
    workflow.add_node(
        "researcher",
        researcher_node,
        retry=get_retry_policy(),
        timeout=get_node_timeout(),
        error_handler=handle_node_failure,
    )
    workflow.add_node(
        "coder",
        coder_node,
        retry=get_retry_policy(),
        timeout=get_node_timeout(),
        error_handler=handle_node_failure,
    )
    workflow.add_node(
        "reviewer",
        reviewer_node,
        retry=get_retry_policy(),
        timeout=get_node_timeout(),
        error_handler=handle_node_failure,
    )

    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "coder")
    workflow.add_edge("coder", "reviewer")
    workflow.add_conditional_edges(
        "reviewer", should_revise, {"coder": "coder", "end": END}
    )

    return workflow.compile(checkpointer=get_checkpointer())


app = build_graph()
