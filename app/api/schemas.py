"""Pydantic request/response models."""
from typing import Any

from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    task: str = Field(..., min_length=1, max_length=4000)
    thread_id: str | None = Field(None, max_length=200)
    user_id: str = Field("default", min_length=1, max_length=200)


class RunResponse(BaseModel):
    thread_id: str
    status: str
    final_output: str
    revisions: int
    token_usage: dict


class HealthResponse(BaseModel):
    status: str
    version: str


class ReadinessResponse(BaseModel):
    status: str
    checks: dict[str, str]


class ErrorEnvelope(BaseModel):
    error: dict[str, Any]


class TokenRequest(BaseModel):
    subject: str = Field(..., min_length=1, max_length=200)
    scopes: list[str] = Field(default_factory=list)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str
