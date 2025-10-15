from __future__ import annotations

import os
import traceback
from datetime import datetime
from fastapi.responses import JSONResponse
from typing import Any

try:
    # If Pydantic is available, use its typing to detect models
    from pydantic import BaseModel  # type: ignore
except Exception:  # pragma: no cover
    BaseModel = object

# Toggle tracebacks via env var; default ON for local dev.
_INCLUDE_TRACEBACK = os.getenv("PRACTICE_INCLUDE_TRACEBACK", "1") not in {
    "0",
    "false",
    "False",
}


def _normalize_payload(payload: Any) -> dict[str, Any]:
    """
    Accepts a pydantic BaseModel, dict, or anything else
    Returns a JSON-serializable dict
    """
    if payload is None:
        return {}

    # Pydantic v2 models
    if isinstance(payload, BaseModel) and hasattr(payload, "model_dump"):
        return payload.model_dump()  # type: ignore[attr-defined]

    # Pydantic v1 models (just in case)
    if isinstance(payload, BaseModel) and hasattr(payload, "dict"):
        return payload.dict()

    if isinstance(payload, dict):
        return payload

    # Last resort: represent minimally
    return {"context": str(payload)}


def _now() -> str:
    return datetime.now().isoformat()


def success_response(
    data: Any,
    message: str = "Operation completed successfully.",
    payload: Any | None = None,
) -> dict[str, Any]:
    """
    Standardize successful API responses

    :param data: Primary payload (pytest results, summaries, etc.)
    :param message: Success message
    :param payload: Optional context (e.g., module, test stats, timing)
    :return: JSON dict containing standardized result details
    """
    return {
        "success": True,
        "timestamp": _now(),
        "message": message,
        "data": data,
        "metadata": _normalize_payload(payload),
    }


def error_response(
    status_code: int,
    message: str,
    payload: Any | None = None,
) -> JSONResponse:
    """
    Standardized error envelope. Accepts an exception string.
    Includes traceback when PRACTICE_INCLUDE_TRACEBACK is truthy.

    :param status_code: HTTP status code
    :param message: Error message.
    :param payload: Optional context (e.g., module, test stats, timing).
    :return: Standardized JSON dict.
    """
    body: dict[str, Any] = {
        "success": False,
        "timestamp": _now(),
        "error": message,
        "data": None,
        "metadata": _normalize_payload(payload),
    }
    if _INCLUDE_TRACEBACK:
        body["traceback"] = traceback.format_exc()
    return JSONResponse(status_code=status_code, content=body)
