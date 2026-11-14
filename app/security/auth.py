"""FastAPI authentication dependencies."""
from fastapi import Header, Security
from fastapi.security import APIKeyHeader

from app.config import settings
from app.core.exceptions import AuthenticationError
from app.security.jwt_handler import verify_token

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


async def verify_api_key(x_api_key: str | None = Security(api_key_header)) -> str:
    """API key auth — for service-to-service calls."""
    if not x_api_key or x_api_key != settings.agentflow_api_key:
        raise AuthenticationError("Invalid or missing API key")
    return x_api_key


async def verify_jwt(authorization: str = Header(...)) -> dict:
    """Bearer JWT verification — for user-scoped calls."""
    if not authorization.startswith("Bearer "):
        raise AuthenticationError("Missing Bearer token")
    token = authorization.removeprefix("Bearer ").strip()
    try:
        return verify_token(token, expected_type="access")
    except ValueError as exc:
        raise AuthenticationError(str(exc))
