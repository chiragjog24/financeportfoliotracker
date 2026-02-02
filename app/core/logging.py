import logging
import sys
from typing import Any, Dict

import structlog

from app.core.config import get_settings

settings = get_settings()


def setup_logging() -> None:
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            (
                structlog.dev.ConsoleRenderer()
                if settings.log_format == "console"
                else structlog.processors.JSONRenderer()
            ),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        logging.getLogger(logger_name).handlers = []


def get_logger(name: str = __name__) -> structlog.BoundLogger:
    return structlog.get_logger(name)


def log_request(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    extra: Dict[str, Any] = None,
) -> None:
    logger = get_logger("api.request")
    log_data = {
        "method": method,
        "path": path,
        "status_code": status_code,
        "duration_ms": round(duration_ms, 2),
    }
    if extra:
        log_data.update(extra)
    logger.info("request_completed", **log_data)


def log_error(
    error_type: str,
    message: str,
    extra: Dict[str, Any] = None,
) -> None:
    logger = get_logger("api.error")
    log_data = {
        "error_type": error_type,
        "message": message,
    }
    if extra:
        log_data.update(extra)
    logger.error("error_occurred", **log_data)
