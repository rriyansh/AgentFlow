"""Custom exception hierarchy for consistent error handling."""
from typing import Any


class AgentFlowError(Exception):
    """Base exception — every custom error inherits from this."""

    status_code: int = 500
    error_code: str = "internal_error"

    def __init__(
        self,
        message: str,
        *,
        details: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.message = message
        self.details = details or {}
        self.headers = headers or {}
        super().__init__(message)


class ValidationError(AgentFlowError):
    status_code = 422
    error_code = "validation_error"


class AuthenticationError(AgentFlowError):
    status_code = 401
    error_code = "authentication_error"


class AuthorizationError(AgentFlowError):
    status_code = 403
    error_code = "authorization_error"


class NotFoundError(AgentFlowError):
    status_code = 404
    error_code = "not_found"


class ConflictError(AgentFlowError):
    status_code = 409
    error_code = "conflict"


class RateLimitError(AgentFlowError):
    status_code = 429
    error_code = "rate_limit_exceeded"


class WorkflowError(AgentFlowError):
    status_code = 500
    error_code = "workflow_error"


class UpstreamError(AgentFlowError):
    status_code = 502
    error_code = "upstream_error"


class ServiceUnavailableError(AgentFlowError):
    status_code = 503
    error_code = "service_unavailable"
