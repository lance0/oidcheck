# oidcheck/server.py
from flask import Flask, render_template, request, flash, jsonify, g
from pydantic import ValidationError
from .validator import validate_config
from .models import AppConfig
from .logging_config import setup_structured_logging, log_validation_event
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
import uuid
import os

app = Flask(__name__)


def validate_environment():
    """Validate required environment variables at startup."""
    required_vars = []

    missing_vars = [var for var in required_vars if not os.environ.get(var)]

    if missing_vars:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

    # Warn about optional but recommended variables
    if not os.environ.get("FLASK_SECRET_KEY"):
        app.logger.warning(
            "FLASK_SECRET_KEY not set, using random key. Set this for production."
        )


# Validate environment on startup
validate_environment()

app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(32)

# Setup structured logging
logger = setup_structured_logging()

# Setup CSRF protection
csrf = CSRFProtect(app)


# Generate correlation ID for each request
@app.before_request
def before_request():
    """Generate correlation ID for request tracking."""
    g.correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    g.request_start_time = request.environ.get("REQUEST_TIME", 0)


limiter = Limiter(
    get_remote_address, app=app, default_limits=["200 per day", "50 per hour"]
)


@app.route("/health")
def health():
    """Health check endpoint for monitoring and load balancer checks.

    Returns:
        JSON response indicating the service health status and dependency checks
    """
    health_status = {
        "status": "healthy",
        "checks": {
            "app": "ok",
            "csrf": "ok" if csrf else "warning",
            "limiter": "ok" if limiter else "warning",
        },
    }

    # Check if we can initialize the logging system
    try:
        logger.info("Health check performed")
        health_status["checks"]["logging"] = "ok"
    except Exception:
        health_status["checks"]["logging"] = "error"
        health_status["status"] = "degraded"

    # Check MSAL availability
    try:
        import msal  # noqa: F401

        health_status["checks"]["msal"] = "ok"
    except ImportError:
        health_status["checks"]["msal"] = "error"
        health_status["status"] = "unhealthy"

    status_code = 200 if health_status["status"] == "healthy" else 503
    return jsonify(health_status), status_code


@app.route("/", methods=["GET", "POST"])
@limiter.limit("10/minute")
def index() -> str:
    """Main route for the OIDC configuration validator web interface.

    Handles both GET requests (displaying the form) and POST requests
    (processing and validating configuration data).

    Returns:
        Rendered HTML template with validation results if applicable
    """
    results = []
    config_text = ""
    if request.method == "POST":
        config_text = request.form.get("config", "")
        if len(config_text) > 10000:
            flash(
                "Configuration is too large. Please limit to 10000 characters.",
                "error",
            )
            return render_template(
                "index.html", results=results, config_text=config_text
            )

        config_dict = {}
        for line in config_text.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                config_dict[key.strip()] = value.strip()

        try:
            config = AppConfig.model_validate(config_dict)
            results = validate_config(config)

            # Log the validation event for audit trail
            log_validation_event(
                logger,
                get_remote_address(),
                "web_form",
                results,
                g.correlation_id,
            )

        except ValidationError as e:
            error_msg = f"Configuration validation error: {e}"
            flash(error_msg, "error")
            logger.error(
                "Configuration validation failed",
                extra={
                    "user_ip": get_remote_address(),
                    "error": str(e),
                    "correlation_id": g.correlation_id,
                },
            )
        except (ValueError, KeyError) as e:
            error_msg = f"Invalid configuration format: {e}"
            flash(error_msg, "error")
            logger.error(
                "Configuration format error",
                extra={
                    "user_ip": get_remote_address(),
                    "error": str(e),
                    "correlation_id": g.correlation_id,
                },
            )
        except RuntimeError as e:
            error_msg = f"Service temporarily unavailable: {e}"
            flash(error_msg, "error")
            logger.error(
                "Service runtime error",
                extra={
                    "user_ip": get_remote_address(),
                    "error": str(e),
                    "correlation_id": g.correlation_id,
                },
            )
        except Exception as e:
            error_msg = f"Unexpected error during validation: {e}"
            flash(error_msg, "error")
            logger.error(
                "Unexpected validation error",
                extra={
                    "user_ip": get_remote_address(),
                    "error": str(e),
                    "correlation_id": g.correlation_id,
                },
            )

    return render_template("index.html", results=results, config_text=config_text)


@app.after_request
def after_request(response):
    """Add correlation ID to response headers for request tracking."""
    response.headers["X-Correlation-ID"] = g.correlation_id
    return response


if __name__ == "__main__":
    app.run(debug=True)
