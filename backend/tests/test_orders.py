import pytest

def test_health_check(client):
    response = client.get("/")
    if response.status_code != 200:
        pytest.fail(f"Health check failed — expected 200, got {response.status_code}")
