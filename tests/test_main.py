import pytest
from oidcheck.main import main
from unittest.mock import patch, MagicMock
import sys
from io import StringIO


def test_main_with_valid_file():
    """Test main function with a valid configuration file."""
    mock_config = {
        "CLIENT_ID": "test-client-id",
        "CLIENT_SECRET": "test-client-secret",
        "TENANT_ID": "test-tenant-id",
        "AUTHORITY": "https://login.microsoftonline.com/test-tenant-id",
        "REDIRECT_URI": "https://localhost/callback",
        "SCOPE": "openid profile",
        "LOG_LEVEL": "INFO",
    }

    with patch("oidcheck.main.dotenv_values", return_value=mock_config):
        with patch("oidcheck.main.validate_config_async") as mock_validate:
            mock_validate.return_value = [
                {"level": "INFO", "message": "Validation successful"}
            ]

            # Mock sys.argv to avoid parsing pytest arguments
            with patch("sys.argv", ["oidcheck"]):
                # Capture stdout
                captured_output = StringIO()
                with patch("sys.stdout", captured_output):
                    main()

                output = captured_output.getvalue()
                assert "INFO" in output
                assert "Validation successful" in output


def test_main_with_json_output():
    """Test main function with JSON output."""
    mock_config = {
        "CLIENT_ID": "test-client-id",
        "CLIENT_SECRET": "test-client-secret",
        "TENANT_ID": "test-tenant-id",
        "AUTHORITY": "https://login.microsoftonline.com/test-tenant-id",
        "REDIRECT_URI": "https://localhost/callback",
        "SCOPE": "openid profile",
        "LOG_LEVEL": "INFO",
    }

    with patch("oidcheck.main.dotenv_values", return_value=mock_config):
        with patch("oidcheck.main.validate_config_async") as mock_validate:
            mock_validate.return_value = [
                {"level": "INFO", "message": "Validation successful"}
            ]

            # Mock sys.argv for JSON output
            with patch("sys.argv", ["oidcheck", "--json"]):
                captured_output = StringIO()
                with patch("sys.stdout", captured_output):
                    main()

                output = captured_output.getvalue()
                assert '"level": "INFO"' in output
                assert '"message": "Validation successful"' in output


def test_main_with_strict_mode_no_errors():
    """Test main function in strict mode with no errors."""
    mock_config = {
        "CLIENT_ID": "test-client-id",
        "CLIENT_SECRET": "test-client-secret",
        "TENANT_ID": "test-tenant-id",
        "AUTHORITY": "https://login.microsoftonline.com/test-tenant-id",
        "REDIRECT_URI": "https://localhost/callback",
        "SCOPE": "openid profile",
        "LOG_LEVEL": "INFO",
    }

    with patch("oidcheck.main.dotenv_values", return_value=mock_config):
        with patch("oidcheck.main.validate_config_async") as mock_validate:
            mock_validate.return_value = [
                {"level": "INFO", "message": "Validation successful"}
            ]

            with patch("sys.argv", ["oidcheck", "--strict"]):
                with patch("sys.exit") as mock_exit:
                    main()
                    mock_exit.assert_not_called()


def test_main_with_strict_mode_with_errors():
    """Test main function in strict mode with errors."""
    mock_config = {
        "CLIENT_ID": "test-client-id",
        "CLIENT_SECRET": "test-client-secret",
        "TENANT_ID": "test-tenant-id",
        "AUTHORITY": "https://login.microsoftonline.com/test-tenant-id",
        "REDIRECT_URI": "https://localhost/callback",
        "SCOPE": "openid profile",
        "LOG_LEVEL": "INFO",
    }

    with patch("oidcheck.main.dotenv_values", return_value=mock_config):
        with patch("oidcheck.main.validate_config_async") as mock_validate:
            mock_validate.return_value = [
                {"level": "ERROR", "message": "Configuration error"}
            ]

            with patch("sys.argv", ["oidcheck", "--strict"]):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
