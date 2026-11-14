import pytest

from app.security.jwt_handler import (
    issue_access_token,
    issue_refresh_token,
    verify_token,
)


def test_issue_and_verify_access_token():
    token, ttl = issue_access_token("user-123", scopes=["read"])
    claims = verify_token(token)
    assert claims["sub"] == "user-123"
    assert claims["scopes"] == ["read"]
    assert ttl > 0


def test_verify_wrong_type():
    refresh, _ = issue_refresh_token("user-123")
    with pytest.raises(ValueError):
        verify_token(refresh, expected_type="access")


def test_invalid_token():
    with pytest.raises(ValueError):
        verify_token("not-a-jwt", expected_type="access")


@pytest.mark.asyncio
async def test_token_endpoint(client):
    r = await client.post("/v1/auth/token", json={"subject": "u1"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "Bearer"
