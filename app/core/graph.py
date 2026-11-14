"""StateGraph definition with fault tolerance."""
from langgraph.graph import END, StateGraph

from app.agents.coder import coder_node
from app.agents.researcher import researcher_node
from app.agents.reviewer import reviewer_node
from app.core.checkpointer import get_checkpointer
from app.core.fault_tolerance import (
    get_retry_policy,
    get_timeout_policy,
    handle_node_failure,
)
from app.core.routing import should_revise
from app.core.state import AgentFlowState


def build_graph() -> StateGraph:
    workflow = StateGraph(AgentFlowState)

    for name, node in (
        ("researcher", researcher_node),
        ("coder", coder_node),
        ("reviewer", reviewer_node),
    ):
        workflow.add_node(
            name,
            node,
            retry_policy=get_retry_policy(),
            timeout=get_timeout_policy(),
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
