from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime
from typing import Any


class JsonFormatter(logging.Formatter):
    """
    Minimal JSON formatter (no external deps).
    """

    def format(self, record: logging.LogRecord) -> str:  # noqa: D401
        payload: dict[str, Any] = {
            "ts": datetime.utcfromtimestamp(record.created).isoformat(timespec="milliseconds")
            + "Z",
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
        # If exception info is present, include it
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


class ConsoleFormatter(logging.Formatter):
    """
    Human-friendly single-line console formatter.
    """

    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.utcfromtimestamp(record.created).isoformat(timespec="seconds") + "Z"
        base = f"{ts} | {record.levelname:<7} | {record.name} | {record.getMessage()}"
        if record.exc_info:
            base += "\n" + self.formatException(record.exc_info)
        return base


def _build_handler(stream, formatter: logging.Formatter) -> logging.Handler:
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
    root.addHandler(_build_handler(sys.stdout, console_formatter))

    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(JsonFormatter())
        root.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
