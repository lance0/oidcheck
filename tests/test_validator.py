# tests/test_validator.py
import pytest
from oidcheck.models import AppConfig
from oidcheck.validator import validate_config


@pytest.fixture
def base_config():
    """A valid base configuration."""
    return {
        "client_id": "test-client-id",
        "client_secret": "test-client-secret",
        "tenant_id": "test-tenant-id",
        "authority": "https://login.microsoftonline.com/test-tenant-id",
        "redirect_uri": "https://localhost/callback",
        "scope": ["openid", "profile"],
        "log_level": "INFO",
    }


def test_valid_config(base_config, mocker):
    # Create a mock that can be called and has the expected structure
    mock_app = mocker.Mock()
    mock_app.initiate_auth_code_flow.return_value = {"auth_uri": "http://mock_auth_uri"}
    mocker.patch("msal.ConfidentialClientApplication", return_value=mock_app)

    config = AppConfig(**base_config)
    results = validate_config(config)

    # A truly valid config should not have errors or warnings
    # We will filter out the INFO message about secret storage for this test
    filtered_results = [r for r in results if "Azure Key Vault" not in r["message"]]
    assert not any(r["level"] in ["ERROR", "WARNING"] for r in filtered_results)
    assert any("Successfully initialized MSAL" in r["message"] for r in results)


def test_missing_client_id(base_config, mocker):
    # Mock the MSAL app to see the validator's logic, not MSAL's
    mock_msal_app = mocker.patch("msal.ConfidentialClientApplication")
    base_config["client_id"] = None
    config = AppConfig(**base_config)
    results = validate_config(config)
    # We expect our validator to catch this before even calling MSAL
    assert not mock_msal_app.called


def test_msal_initialization_failure(base_config, mocker):
    # Simulate MSAL raising an exception
    mocker.patch(
        "msal.ConfidentialClientApplication",
        side_effect=ValueError("Invalid authority"),
    )
    config = AppConfig(**base_config)
    results = validate_config(config)
    assert any(
        "Failed to initialize MSAL client: Invalid authority" in r["message"]
        for r in results
    )


def test_non_https_redirect_uri(base_config, mocker):
    mocker.patch("msal.ConfidentialClientApplication")
    base_config["redirect_uri"] = "http://localhost/callback"
    config = AppConfig(**base_config)
    results = validate_config(config)
    assert any("REDIRECT_URI is not using HTTPS" in r["message"] for r in results)


def test_debug_log_level(base_config, mocker):
    mocker.patch("msal.ConfidentialClientApplication")
    base_config["log_level"] = "DEBUG"
    config = AppConfig(**base_config)
    results = validate_config(config)
    assert any("log sensitive information" in r["message"] for r in results)


def test_gcc_high_authority_mismatch(base_config, mocker):
    mocker.patch("msal.ConfidentialClientApplication")
    base_config["authority"] = "https://login.microsoftonline.com/test-tenant-id"
    base_config["tenant_id"] = "tenant.onmicrosoft.us"  # GCC-High tenant
    config = AppConfig(**base_config)
    results = validate_config(config)
    assert any("US Government environment" in r["message"] for r in results)


def test_missing_openid_scope(base_config, mocker):
    mocker.patch("msal.ConfidentialClientApplication")
    base_config["scope"] = ["profile"]
    config = AppConfig(**base_config)
    results = validate_config(config)
    assert any("SCOPE is missing 'openid'" in r["message"] for r in results)
