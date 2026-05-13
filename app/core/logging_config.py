# Built by AbilitySoft | abilitysoft.net
"""
Structured logging configuration.

Configures the standard library ``logging`` module with a JSON-friendly
formatter suitable for production log aggregation (ELK, CloudWatch, etc.).
"""

import logging
import sys
from typing import Optional

from app.core.config import get_settings

settings = get_settings()


class JsonFormatter(logging.Formatter):
    """
    A simple JSON log formatter for structured log output.

    Produces one JSON object per log line for easy parsing by
    log aggregation tools.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            A JSON-formatted log string.
        """
        import json
        from datetime import datetime, timezone

        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info and record.exc_info[1]:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging(log_level: Optional[str] = None) -> None:
    """
    Configure application-wide logging.

    In production mode, outputs structured JSON logs.
    In development mode, outputs human-readable coloured logs.

    Args:
        log_level: Override log level (e.g. ``"DEBUG"``).
                   Defaults to ``settings.LOG_LEVEL``.
    """
    level = getattr(logging, (log_level or settings.LOG_LEVEL).upper(), logging.INFO)

    # Remove any existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)

    if settings.ENVIRONMENT == "development":
        # Human-readable format for local development
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d — %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        # Structured JSON for production
        formatter = JsonFormatter()

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(level)

    # Quieten noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.DB_ECHO_LOG else logging.WARNING
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger instance.

    Args:
        name: Logger name — typically ``__name__`` of the calling module.

    Returns:
        A configured ``logging.Logger``.
    """
    return logging.getLogger(name)
