from typing import Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.agents.base import BaseAgent
from app.tools.code_execution import execute_code
from app.observability.tracing import trace_node


class CoderAgent(BaseAgent):
    """Writes and validates code using the execution sandbox."""

    def __init__(self) -> None:
        super().__init__(temperature=0.0)
        self.llm_with_tools = self.llm.bind_tools([execute_code])

    @trace_node("coder")
    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        feedback = state.get("review_feedback", "None")
        system = SystemMessage(content=(
            "You are a Senior Software Engineer. Write clean, production-ready code. "
            "Use the execute_code tool to verify your solution before returning it. "
            "Address any reviewer feedback if provided."
        ))
        user = HumanMessage(content=(
            f"Task: {state['messages'][0].content}\n\n"
            f"Research findings:\n{state['research_findings']}\n\n"
            f"Previous review feedback: {feedback}"
        ))
        response = self.llm_with_tools.invoke([system, user])

        return {
            "code_output": response.content,
            "messages": [AIMessage(content=response.content, name="Coder")],
            "token_usage": {"coder": response.usage_metadata or {}},
        }


_coder = CoderAgent()
coder_node = _coder.run
