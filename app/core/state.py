"""Shared graph state and structured output models."""
import operator
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field


class AgentFlowState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    research_findings: str
    code_output: str
    review_status: str
    review_feedback: str
    revision_count: int
    thread_id: str
    user_id: str
    token_usage: Annotated[dict, lambda a, b: {**a, **b}]


class ReviewDecision(BaseModel):
    status: str = Field(description="Either APPROVED or NEEDS_REVISION")
    feedback: str = Field(description="Specific, actionable feedback")
