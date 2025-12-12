import copy
import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def restore_activities():
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))


def test_get_activities_returns_data(client):
    response = client.get("/activities")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Basketball Team" in payload


def test_signup_adds_participant(client):
    activity = "Science Club"
    email = "newstudent@example.com"

    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200

    data = response.json()
    assert "Signed up" in data.get("message", "")
    assert email in app_module.activities[activity]["participants"]
