from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.nodes import agent_node, tool_node


def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)
    builder.add_node("tool", tool_node)
    builder.add_edge("agent", "tool")
    builder.add_edge("tool", END)
    builder.set_entry_point("agent")
    return builder.compile()
