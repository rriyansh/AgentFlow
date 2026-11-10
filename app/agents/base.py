from abc import ABC, abstractmethod
from typing import Any
from langchain_openai import ChatOpenAI
from app.config import settings


class BaseAgent(ABC):
    """Base class for all specialized agents."""

    def __init__(self, temperature: float = 0.0) -> None:
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=temperature,
            api_key=settings.openai_api_key,
            timeout=settings.agent_timeout_seconds,
            max_retries=2,
        )

    @abstractmethod
    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute agent logic and return state updates."""
        ...
