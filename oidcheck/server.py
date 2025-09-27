# oidcheck/server.py
from flask import Flask, render_template, request, flash, jsonify
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
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or os.urandom(32)

# Setup structured logging
logger = setup_structured_logging()

# Setup CSRF protection
csrf = CSRFProtect(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


@app.route("/", methods=["GET", "POST"])
@limiter.limit("10/minute")
def index() -> str:
    results = []
    config_text = ""
    if request.method == "POST":
        config_text = request.form.get("config", "")
        if len(config_text) > 10000:
            flash("Configuration is too large. Please limit to 10000 characters.", "error")
            return render_template("index.html", results=results, config_text=config_text)

        config_dict = {}
        for line in config_text.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                config_dict[key.strip()] = value.strip()

        try:
            config = AppConfig.model_validate(config_dict)
            results = validate_config(config)

            # Log the validation event for audit trail
            request_id = str(uuid.uuid4())
            log_validation_event(
                logger,
                get_remote_address(),
                "web_form",
                results,
                request_id
            )

        except ValidationError as e:
            error_msg = f"Configuration validation error: {e}"
            flash(error_msg, "error")
            logger.error(
                "Configuration validation failed",
                extra={
                    "user_ip": get_remote_address(),
                    "error": str(e),
                    "request_id": str(uuid.uuid4())
                }
            )
        except Exception as e:
            error_msg = f"Unexpected error during validation: {e}"
            flash(error_msg, "error")
            logger.error(
                "Unexpected validation error",
                extra={
                    "user_ip": get_remote_address(),
                    "error": str(e),
                    "request_id": str(uuid.uuid4())
                }
            )


    return render_template("index.html", results=results, config_text=config_text)

if __name__ == "__main__":
    app.run(debug=True)

