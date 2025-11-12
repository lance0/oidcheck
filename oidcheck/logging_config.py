# oidcheck/logging_config.py
import logging
import json
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional


class StructuredFormatter(logging.Formatter):
    """Custom formatter that outputs structured JSON logs for audit trails."""  # noqa: E501

    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if present
        if hasattr(record, "user_ip"):
            log_entry["user_ip"] = record.user_ip  # type: ignore
        if hasattr(record, "config_validation"):
            log_entry["config_validation"] = record.config_validation  # type: ignore  # noqa: E501
        if hasattr(record, "validation_results"):
            log_entry["validation_results"] = record.validation_results  # type: ignore  # noqa: E501
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id  # type: ignore

        return json.dumps(log_entry)


def setup_structured_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Sets up structured logging for audit trails.
    """
    logger = logging.getLogger("oidcheck")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create console handler with structured formatter
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())
    logger.addHandler(handler)

    return logger


def log_validation_event(
    logger: logging.Logger,
    user_ip: str,
    config_source: str,
    results: List[Dict[str, Any]],
    request_id: Optional[str] = None,
) -> None:
    """
    Log a configuration validation event with structured data.
    """
    logger.info(
        "Configuration validation completed",
        extra={
            "user_ip": user_ip,
            "config_validation": {
                "source": config_source,
                "error_count": len([r for r in results if r["level"] == "ERROR"]),  # noqa: E501
                "warning_count": len([r for r in results if r["level"] == "WARNING"]),  # noqa: E501
                "info_count": len([r for r in results if r["level"] == "INFO"]),
            },
            "validation_results": results,
            "request_id": request_id,
        },
    )
