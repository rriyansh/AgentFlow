"""Token issuance and refresh endpoints."""
from fastapi import APIRouter

from app.api.schemas import (
    RefreshRequest,
    TokenRequest,
    TokenResponse,
)
from app.core.exceptions import AuthenticationError
from app.security.jwt_handler import (
    issue_access_token,
    issue_refresh_token,
    verify_token,
)

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
async def create_token(payload: TokenRequest) -> TokenResponse:
    """
    Issue access + refresh tokens for a subject.

    NOTE: In production, protect this endpoint behind an identity provider
    (OAuth2/OIDC) or a shared secret. Left open here for demo/dev usage.
    """
    access, access_ttl = issue_access_token(payload.subject, scopes=payload.scopes)
    refresh, _ = issue_refresh_token(payload.subject)
    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        expires_in=access_ttl,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(payload: RefreshRequest) -> TokenResponse:
    try:
        claims = verify_token(payload.refresh_token, expected_type="refresh")
    except ValueError as exc:
        raise AuthenticationError(str(exc))
    subject = claims["sub"]
    access, access_ttl = issue_access_token(subject)
    new_refresh, _ = issue_refresh_token(subject)
    return TokenResponse(
        access_token=access,
        refresh_token=new_refresh,
        expires_in=access_ttl,
    )
