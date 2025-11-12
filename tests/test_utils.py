import pytest
from oidcheck.utils import format_validation_results, load_config_from_file
from unittest.mock import patch


def test_format_validation_results_text():
    """Test formatting validation results as text."""
    results = [
        {"level": "INFO", "message": "Test info message"},
        {"level": "WARNING", "message": "Test warning message"},
        {"level": "ERROR", "message": "Test error message"},
    ]

    formatted = format_validation_results(results, output_format="text")
    lines = formatted.strip().split("\n")

    assert "[INFO] Test info message" in lines
    assert "[WARNING] Test warning message" in lines
    assert "[ERROR] Test error message" in lines


def test_format_validation_results_json():
    """Test formatting validation results as JSON."""
    results = [
        {"level": "INFO", "message": "Test info message"},
        {"level": "WARNING", "message": "Test warning message"},
    ]

    formatted = format_validation_results(results, output_format="json")
    import json

    parsed = json.loads(formatted)

    assert len(parsed) == 2
    assert parsed[0]["level"] == "INFO"
    assert parsed[0]["message"] == "Test info message"
    assert parsed[1]["level"] == "WARNING"
    assert parsed[1]["message"] == "Test warning message"


def test_format_validation_results_html():
    """Test formatting validation results as HTML."""
    results = [
        {"level": "INFO", "message": "Test info message"},
        {"level": "WARNING", "message": "Test warning message"},
    ]

    formatted = format_validation_results(results, output_format="html")

    assert 'class="result-info"' in formatted
    assert 'class="result-warning"' in formatted
    assert "Test info message" in formatted
    assert "Test warning message" in formatted


def test_load_config_from_file():
    """Test loading configuration from file."""
    mock_config = {
        "CLIENT_ID": "test-client-id",
        "CLIENT_SECRET": "test-client-secret",
        "TENANT_ID": "test-tenant-id",
        "AUTHORITY": "https://login.microsoftonline.com/test-tenant-id",
        "REDIRECT_URI": "https://localhost/callback",
        "SCOPE": "openid profile",
        "LOG_LEVEL": "INFO",
    }

    with patch("dotenv.dotenv_values", return_value=mock_config):
        config = load_config_from_file(".env")

        assert config["CLIENT_ID"] == "test-client-id"
        assert config["CLIENT_SECRET"] == "test-client-secret"
        assert config["TENANT_ID"] == "test-tenant-id"


def test_load_config_from_file_not_found():
    """Test loading configuration from non-existent file."""
    with patch("dotenv.dotenv_values", return_value={}):
        config = load_config_from_file("nonexistent.env")

        assert config == {}


def test_load_config_from_file_with_empty_values():
    """Test loading configuration file with empty values."""
    mock_config = {
        "CLIENT_ID": "",
        "CLIENT_SECRET": None,
        "TENANT_ID": "test-tenant-id",
    }

    with patch("dotenv.dotenv_values", return_value=mock_config):
        config = load_config_from_file(".env")

        assert config["CLIENT_ID"] == ""
        assert config["CLIENT_SECRET"] is None
        assert config["TENANT_ID"] == "test-tenant-id"
