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
    Accepts a pydantic BaseModel, dict, or anything else.
    Returns a JSON-serializable dict. Recursively normalizes nested BaseModels.
    """
    if payload is None:
        return {}

    # Helper to recursively convert nested structures
    def _coerce(obj: Any) -> Any:
        # Pydantic v2 model
        if isinstance(obj, BaseModel) and hasattr(obj, "model_dump"):
            return obj.model_dump()  # type: ignore[attr-defined]
        # Pydantic v1 model (defensive)
        if isinstance(obj, BaseModel) and hasattr(obj, "dict"):
            return obj.dict()
        # dict: normalize values
        if isinstance(obj, dict):
            return {k: _coerce(v) for k, v in obj.items()}
        # Sequence types
        if isinstance(obj, (list, tuple, set)):
            return [_coerce(v) for v in obj]
        # Passthrough for JSON-serializable primitives
        return obj

    # Top-level cases
    if isinstance(payload, BaseModel):
        return _coerce(payload)  # returns a dict
    if isinstance(payload, dict):
        return _coerce(payload)

    # Last resort: represent minimally
    return {"context": str(payload)}


def _now() -> str:
    return datetime.now().isoformat()


def success_response(
    *,
    data: Any,
    message: str = "Operation completed successfully.",
    payload: Any | None = None,
) -> JSONResponse:
    """
    Standardize successful API responses

    :param data: Primary payload (pytest results, summaries, etc.)
    :param message: Success message
    :param payload: Optional context (e.g., module, test stats, timing)
    :return: JSONResponse object containing standardized result details
    """
    content = {
        "success": True,
        "timestamp": _now(),
        "message": message,
        "data": data,
        "metadata": _normalize_payload(payload),
    }
    return JSONResponse(status_code=200, content=content)


def error_response(
    *,
    status_code: int = 400,
    message: str = "Error",
    payload: dict[str, Any] | None = None,
) -> JSONResponse:
    """
    Standardized error envelope. Accepts an exception string.
    Includes traceback when PRACTICE_INCLUDE_TRACEBACK is truthy.

    :param status_code: HTTP status code
    :param message: Error message.
    :param payload: Optional context (e.g., module, test stats, timing).
    :return: JSONResponse object containing standardized error details
    """
    content: dict[str, Any] = {
        "success": False,
        "timestamp": _now(),
        "message": message,
        "data": None,
        "metadata": _normalize_payload(payload),
    }
    if _INCLUDE_TRACEBACK:
        content["traceback"] = traceback.format_exc()
    return JSONResponse(status_code=status_code, content=content)


# ---------- Shared helpers for pytest result presentation ----------


def format_pytest_summary_tail(
    summary: dict[str, Any] | None,
    keys: tuple[str, ...] = ("failed", "errors", "skipped", "collected", "deselected"),
) -> str:
    """
    Build a compact tail like " (failed=1, errors=0, collected=6)". Returns "" if nothing to show.
    Only includes keys present in the summary and with a truthy/meaningful value (non-None).
    """
    if not isinstance(summary, dict):
        return ""
    parts: list[str] = []
    for k in keys:
        v = summary.get(k)
        # Include ints/floats; skip None/missing. Keep 0 for context on totals like 'collected'.
        if isinstance(v, int | float) or v == 0:
            parts.append(f"{k}={v}")
    return f" ({', '.join(parts)})" if parts else ""


def is_pytest_ok(result: dict[str, Any]) -> bool:
    """
    Canonical success check: pytest 'success' flag AND exit_code==0.
    """
    try:
        return bool(result.get("success") is True and int(result.get("exit_code", 1)) == 0)
    except Exception:
        return False
