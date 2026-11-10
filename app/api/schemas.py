from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    task: str = Field(..., min_length=1, max_length=4000)
    thread_id: str | None = None
    user_id: str = "default"


class RunResponse(BaseModel):
    thread_id: str
    status: str
    final_output: str
    revisions: int
    token_usage: dict


class HealthResponse(BaseModel):
    status: str
    version: str
