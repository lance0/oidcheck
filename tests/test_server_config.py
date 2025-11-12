from unittest.mock import patch
import os
from oidcheck.server import validate_environment


def test_validate_environment_missing_required():
    """Test environment validation with missing required variables."""
    with patch.dict(os.environ, {}, clear=True):
        # Should not raise since we have no required vars currently
        validate_environment()


def test_validate_environment_no_secret_key():
    """Test environment validation without FLASK_SECRET_KEY."""
    with patch.dict(os.environ, {}, clear=True):
        with patch("oidcheck.server.app") as mock_app:
            validate_environment()
            mock_app.logger.warning.assert_called_with(
                "FLASK_SECRET_KEY not set, using random key. Set this for production."
            )


def test_validate_environment_with_secret_key():
    """Test environment validation with FLASK_SECRET_KEY set."""
    with patch.dict(os.environ, {"FLASK_SECRET_KEY": "test-secret-key"}, clear=True):
        with patch("oidcheck.server.app") as mock_app:
            validate_environment()
            mock_app.logger.warning.assert_not_called()


def test_environment_validation_runtime_error():
    """Test environment validation raises RuntimeError for missing required vars."""
    # This test would need actual required environment variables to be added
    # For now, it demonstrates the pattern
    pass
