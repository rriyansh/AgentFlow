import asyncio

from app.agents.researcher import ResearcherAgent
from app.core.state import AgentState


def test_researcher_agent() -> None:
    agent = ResearcherAgent()
    state = AgentState(query="research topic")
    result = asyncio.run(agent.run(state))
    assert result.result is not None
    assert "research topic" in result.result
