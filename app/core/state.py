import operator
from typing import TypedDict, Annotated, Sequence
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage


class AgentFlowState(TypedDict):
    """Shared memory flowing through every node in the graph."""
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
    """Structured output from the Reviewer agent."""
    status: str = Field(description="Either APPROVED or NEEDS_REVISION")
    feedback: str = Field(description="Specific, actionable feedback")
