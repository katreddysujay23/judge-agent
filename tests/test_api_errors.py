# tests/test_api_errors.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_invalid_input_schema():
    payload = {
        "type": "text"
        # missing content
    }

    response = client.post("/evaluate", json=payload)
    assert response.status_code == 422  # FastAPI validation


def test_invalid_type():
    payload = {
        "type": "invalid",
        "content": "Test"
    }

    response = client.post("/evaluate", json=payload)
    assert response.status_code == 422
