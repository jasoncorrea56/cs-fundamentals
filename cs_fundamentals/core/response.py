from __future__ import annotations

import os
import traceback
from datetime import datetime
from typing import Any, Protocol, runtime_checkable

from fastapi.responses import JSONResponse


# Enable traceback in error responses unless explicitly disabled.
_INCLUDE_TRACEBACK = os.getenv("PRACTICE_INCLUDE_TRACEBACK", "1") not in {
    "0",
    "false",
    "False",
}

# ---- Pydantic-compat detection (v1/v2) via Protocols ----


@runtime_checkable
class _SupportsModelDump(Protocol):
    def model_dump(self) -> dict[str, Any]: ...


@runtime_checkable
class _SupportsDict(Protocol):
    def dict(self) -> dict[str, Any]: ...


def _normalize_payload(payload: Any) -> dict[str, Any]:
    """
    Accepts a Pydantic-like model (v1 or v2), dict, or other JSON-serializable payload.
    Returns a JSON-serializable dict. Recursively normalizes nested models/containers.
    """
    if payload is None:
        return {}

    def _coerce(obj: Any) -> Any:
        # Pydantic v2
        if isinstance(obj, _SupportsModelDump):
            try:
                return obj.model_dump()
            except Exception:
                pass
        # Pydantic v1
        if isinstance(obj, _SupportsDict):
            try:
                return obj.dict()
            except Exception:
                pass
        # Dict: normalize values
        if isinstance(obj, dict):
            return {k: _coerce(v) for k, v in obj.items()}
        # Sequence types
        if isinstance(obj, (list, tuple, set)):
            return [_coerce(v) for v in obj]
        # Passthrough for JSON-serializable primitives
        return obj

    # Top-level cases: ensure we always return a dict
    if isinstance(payload, (dict, _SupportsModelDump, _SupportsDict)):
        data = _coerce(payload)
        return data if isinstance(data, dict) else {"context": data}

    return {"context": str(payload)}


def _now() -> str:
    return datetime.now().isoformat()


def success_response(
    *,
    data: Any,
    message: str = "Operation completed successfully.",
    payload: Any | None = None,
) -> JSONResponse:
    """Standardize successful API responses."""
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
    Standardized error envelope.
    Includes traceback when PRACTICE_INCLUDE_TRACEBACK is truthy.
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
        # Include numeric values; keep 0 to show totals like 'collected'.
        if isinstance(v, (int, float)) or v == 0:
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
