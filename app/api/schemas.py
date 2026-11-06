from pydantic import BaseModel


class AgentRunRequest(BaseModel):
    query: str


class AgentRunResponse(BaseModel):
    query: str
    status: str
