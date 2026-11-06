from app.agents.base import BaseAgent
from app.core.state import AgentState


class ResearcherAgent(BaseAgent):
    async def run(self, state: AgentState) -> AgentState:
        state.result = f"Research result for: {state.query}"
        return state
