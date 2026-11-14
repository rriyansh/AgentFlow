"""Researcher agent — gathers info via web search."""
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.agents.base import BaseAgent
from app.observability.tracing import trace_node
from app.tools.web_search import web_search


class ResearcherAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(temperature=0.0)
        self.llm_with_tools = self.llm.bind_tools([web_search])

    @trace_node("researcher")
    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        system = SystemMessage(
            content=(
                "You are a Senior Research Analyst. Use the web_search tool to "
                "gather current, factual information. Return a structured summary."
            )
        )
        user = HumanMessage(
            content=f"Research this task: {state['messages'][-1].content}"
        )
        response = self.llm_with_tools.invoke([system, user])
        return {
            "research_findings": response.content,
            "messages": [AIMessage(content=response.content, name="Researcher")],
            "token_usage": {"researcher": response.usage_metadata or {}},
        }


researcher_node = ResearcherAgent().run
