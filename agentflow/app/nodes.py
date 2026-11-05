from langgraph.graph import StateGraph
from app.state import AgentState
from app.tools import example_tool


def agent_node(state: AgentState) -> AgentState:
    """Agent node function."""
    state["step"] = state.get("step", 0) + 1
    return state


def tool_node(state: AgentState) -> AgentState:
    """Tool node function."""
    result = example_tool.invoke({"input_text": "hello"})
    state["context"] = {"tool_result": result}
    return state
