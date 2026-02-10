import os
import sys
from pathlib import Path

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient

from app import app, activities


def test_get_activities():
    client = TestClient(app)
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_and_duplicate():
    client = TestClient(app)
    email = "pytest-user@example.com"

    # Ensure email not already present
    if email in activities["Basketball"]["participants"]:
        activities["Basketball"]["participants"].remove(email)

    res = client.post(f"/activities/Basketball/signup?email={email}")
    assert res.status_code == 200
    body = res.json()
    assert "Signed up" in body.get("message", "")

    # Duplicate signup should return 400
    res2 = client.post(f"/activities/Basketball/signup?email={email}")
    assert res2.status_code == 400


def test_root_redirect():
    client = TestClient(app)
    res = client.get("/", allow_redirects=False)
    assert res.status_code in (307, 308)
    assert res.headers.get("location") == "/static/index.html"
