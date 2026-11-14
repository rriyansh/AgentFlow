import pytest


@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_healthz(client):
    r = await client.get("/healthz")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_requires_api_key(client):
    r = await client.post(
        "/v1/agent/run", json={"task": "x"}, headers={"x-api-key": "wrong"}
    )
    assert r.status_code == 401
    body = r.json()
    assert body["error"]["code"] == "authentication_error"


@pytest.mark.asyncio
async def test_validation_error(client):
    r = await client.post("/v1/agent/run", json={"task": ""})
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "validation_error"


@pytest.mark.asyncio
async def test_payload_too_large(client):
    r = await client.post(
        "/v1/agent/run",
        json={"task": "x" * 10},
        headers={"content-length": str(10 * 1024 * 1024)},
    )
    assert r.status_code == 413
