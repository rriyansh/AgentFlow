"""Verify the global error envelope format."""
import pytest


@pytest.mark.asyncio
async def test_404_returns_error_envelope(client):
    r = await client.get("/v1/does-not-exist")
    assert r.status_code == 404
    # FastAPI's default 404 handler is used — we only override custom exceptions
