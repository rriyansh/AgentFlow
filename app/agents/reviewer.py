from app.agents.base import BaseAgent
from app.core.state import AgentState


class ReviewerAgent(BaseAgent):
    async def run(self, state: AgentState) -> AgentState:
        state.result = f"Reviewed: {state.result or state.query}"
        return state
