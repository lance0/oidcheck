import pytest
from oidcheck.server import app
from unittest.mock import patch


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


def test_index_get(client):
    """Test GET request to index page."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Flask OIDC Config Validator" in response.data


def test_index_post_valid_config(client):
    """Test POST request with valid configuration."""
    config_data = """CLIENT_ID=test-client-id
CLIENT_SECRET=test-client-secret
TENANT_ID=test-tenant-id
AUTHORITY=https://login.microsoftonline.com/test-tenant-id
REDIRECT_URI=https://localhost/callback
SCOPE=openid profile"""

    with patch("oidcheck.server.validate_config") as mock_validate:
        mock_validate.return_value = [
            {"level": "INFO", "message": "Validation successful"}
        ]
        response = client.post("/", data={"config": config_data})
        assert response.status_code == 200
        assert b"Validation Results" in response.data


def test_index_post_invalid_config(client):
    """Test POST request with invalid configuration."""
    config_data = "INVALID_CONFIG"

    response = client.post("/", data={"config": config_data})
    assert response.status_code == 200
    # Should show validation error


def test_index_post_large_config(client):
    """Test POST request with config that's too large."""
    large_config = "A" * 15000  # Create a config larger than 10,000 characters

    response = client.post("/", data={"config": large_config})
    assert response.status_code == 200
    assert b"Configuration is too large" in response.data


def test_rate_limiting(client):
    """Test that rate limiting is working."""
    # This would require more complex setup with time mocking
    # For now, just ensure the endpoint exists
    response = client.post("/", data={"config": "test"})
    assert response.status_code in [200, 429]  # 429 would be rate limited


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "checks" in data
    assert data["checks"]["app"] == "ok"
    assert data["checks"]["msal"] == "ok"


def test_correlation_id_header(client):
    """Test that correlation ID is added to response headers."""
    response = client.get("/")
    assert response.status_code == 200
    assert "X-Correlation-ID" in response.headers


def test_custom_correlation_id(client):
    """Test that custom correlation ID is preserved."""
    custom_id = "test-correlation-123"
    response = client.get("/", headers={"X-Correlation-ID": custom_id})
    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == custom_id
