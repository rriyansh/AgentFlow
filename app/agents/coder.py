from app.agents.base import BaseAgent
from app.core.state import AgentState


class CoderAgent(BaseAgent):
    async def run(self, state: AgentState) -> AgentState:
        state.result = f"Code generated for: {state.query}"
        return state
