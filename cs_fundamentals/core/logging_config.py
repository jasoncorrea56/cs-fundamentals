from __future__ import annotations

import json
import logging
import os
import sys
from contextvars import ContextVar
from datetime import datetime, UTC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from io import StringIO
    from _pytest.capture import CaptureIO
    from typing import Any

# Request-scoped id (set by middleware)
request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)


class RequestIdFilter(logging.Filter):
    """Inject request_id (if set) into log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Attach request_id even if None so formatters can rely on the attribute existing
        """
        record.request_id = request_id_var.get()
        return True


class JsonFormatter(logging.Formatter):
    """
    Minimal JSON formatter (no external deps).
    """

    def format(self, record: logging.LogRecord) -> str:  # noqa: D401
        payload: dict[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, tz=UTC).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        # Common extras that are helpful for debugging
        payload.update(
            {
                "pid": record.process,
                "tid": record.thread,
                "filename": record.filename,
                "lineno": record.lineno,
                "func": record.funcName,
            }
        )
        # Include request_id when available
        if getattr(record, "request_id", None):
            payload["request_id"] = record.request_id
        # If exception info is present, include it
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


class ConsoleFormatter(logging.Formatter):
    """
    Human-friendly single-line console formatter.
    """

    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.fromtimestamp(record.created, tz=UTC).isoformat(timespec="milliseconds")
        rid = getattr(record, "request_id", None)
        rid_part = f" | rid={rid}" if rid else ""
        base = f"{ts} | {record.levelname:<7} | {record.name}{rid_part} | {record.getMessage()}"
        if record.exc_info:
            base += "\n" + self.formatException(record.exc_info)
        return base


def _build_handler(stream: CaptureIO | StringIO, formatter: logging.Formatter) -> logging.Handler:
    handler = logging.StreamHandler(stream)
    handler.setFormatter(formatter)
    return handler


def configure_logging(*, force: bool = False) -> None:
    """
    Configure root logging once. Respects env vars:
      LOG_LEVEL  (default: INFO)
      LOG_FORMAT (json|console, default: json)
      LOG_FILE   (optional path; if set, also logs to file as JSON)
    """
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    fmt = os.getenv("LOG_FORMAT", "json").lower()
    log_file = os.getenv("LOG_FILE")

    # Avoid duplicate handlers when reloading (uvicorn --reload)
    root = logging.getLogger()
    if root.handlers and not force:
        return

    # Remove any pre-existing handlers
    for h in root.handlers[:]:
        root.removeHandler(h)

    root.setLevel(level)

    console_formatter: logging.Formatter = JsonFormatter() if fmt == "json" else ConsoleFormatter()

    # Build console handler and attach request-id filter
    console_handler = _build_handler(sys.stdout, console_formatter)
    console_handler.addFilter(RequestIdFilter())  # Ensure every log has request_id, if present
    root.addHandler(console_handler)

    # If a log file is configured (not recommended in prod), also attach the filter there
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(JsonFormatter())
        file_handler.addFilter(RequestIdFilter())
        root.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
