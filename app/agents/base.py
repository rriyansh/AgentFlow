from abc import ABC, abstractmethod

from app.core.state import AgentState


class BaseAgent(ABC):
    """Base class for all agents."""

    @abstractmethod
    async def run(self, state: AgentState) -> AgentState:
        raise NotImplementedError
