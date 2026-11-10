from typing import Any
from langchain_core.messages import HumanMessage, SystemMessage
from app.agents.base import BaseAgent
from app.core.state import ReviewDecision
from app.observability.tracing import trace_node


class ReviewerAgent(BaseAgent):
    """Reviews code quality and returns a structured decision."""

    def __init__(self) -> None:
        super().__init__(temperature=0.0)
        self.structured_llm = self.llm.with_structured_output(ReviewDecision)

    @trace_node("reviewer")
    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        system = SystemMessage(content=(
            "You are a meticulous Code Reviewer. Assess quality, security, and "
            "correctness. Return APPROVED only if the code is production-ready. "
            "Otherwise return NEEDS_REVISION with specific, actionable feedback."
        ))
        user = HumanMessage(content=f"Code to review:\n{state['code_output']}")
        decision: ReviewDecision = self.structured_llm.invoke([system, user])

        return {
            "review_status": decision.status,
            "review_feedback": decision.feedback,
            "revision_count": state.get("revision_count", 0) + 1,
        }


_reviewer = ReviewerAgent()
reviewer_node = _reviewer.run
