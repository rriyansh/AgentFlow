import jwt
from fastapi import Header, HTTPException, Security
from fastapi.security import APIKeyHeader
from app.config import settings

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


async def verify_api_key(
    x_api_key: str = Security(api_key_header),
) -> str:
    """API key authentication for agent endpoints."""
    if not x_api_key or x_api_key != settings.agentflow_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


async def verify_jwt(authorization: str = Header(...)) -> dict:
    """JWT bearer token verification for service-to-service calls."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Missing Bearer token"
        )
    token = authorization.removeprefix("Bearer ")
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
