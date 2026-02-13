# tests/test_api_success.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_evaluate_text_success():
    payload = {
        "type": "text",
        "content": "I built this startup after failing twice.",
        "metadata": {"platform": "linkedin"}
    }

    response = client.post("/evaluate", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert "generation_prediction" in body
    assert "virality" in body
    assert "distribution_analysis" in body
    assert "meta_explanation" in body
