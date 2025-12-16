import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data

def test_signup_and_unregister():
    # Use a unique email for testing
    activity = "Basketball"
    email = "testuser@mergington.edu"
    # Ensure not already signed up
    client.delete(f"/activities/{activity}/unregister?email={email}")
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    # Unregister
    response_del = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response_del.status_code == 200
    assert f"Removed {email}" in response_del.json()["message"]
    # Unregister again (should fail)
    response_del2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response_del2.status_code == 404

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404

def test_unregister_invalid_activity():
    response = client.delete("/activities/Nonexistent/unregister?email=foo@bar.com")
    assert response.status_code == 404

def test_unregister_invalid_email():
    response = client.delete("/activities/Basketball/unregister?email=notfound@mergington.edu")
    assert response.status_code == 404
