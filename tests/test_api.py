from fastapi.testclient import TestClient

from app.main import app  # noqa: F401


def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
