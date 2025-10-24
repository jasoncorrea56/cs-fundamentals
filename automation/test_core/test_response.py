from __future__ import annotations

import json
from typing import Any, TYPE_CHECKING
from pydantic import BaseModel

from cs_fundamentals.core import response as resp

if TYPE_CHECKING:
    from starlette.responses import JSONResponse
    import pytest


def _json_of(r: JSONResponse) -> dict[str, Any]:
    return json.loads(r.body.decode("utf-8"))


# ------------------------------- _normalize_payload() -------------------------------


def test_normalize_payload_none() -> None:
    assert resp._normalize_payload(None) == {}


def test_normalize_payload_dict_passthrough() -> None:
    data: dict[str, Any] = {"a": 1}
    out: dict[str, Any] = resp._normalize_payload(data)
    assert out == data
    assert out is not data  # Document: function may return a new dict


def test_normalize_payload_pydantic_v2() -> None:
    class M(BaseModel):
        a: int
        b: str

    m = M(a=1, b="x")
    # v2 path uses model_dump()
    out = resp._normalize_payload(m)
    assert out == {"a": 1, "b": "x"}


def test_normalize_payload_fake_v1_branch() -> None:
    """
    Simulate a v1-style model: has .dict() but no .model_dump().
    """

    class V1Like:
        def __init__(self) -> None:
            self.a = 1

        def dict(self) -> dict[str, Any]:
            return {"a": self.a}

    r = resp.success_response(data={"ok": True}, payload=V1Like())
    body = json.loads(r.body)
    assert body["metadata"] == {"a": 1}


def test_normalize_payload_fake_v2_branch() -> None:
    class V2Like:
        def model_dump(self) -> dict[str, Any]:
            return {"b": 2}

    r = resp.error_response(payload=V2Like())
    body = json.loads(r.body)
    assert body["metadata"] == {"b": 2}


def test_normalize_payload_fallback_other_object() -> None:
    class Thing:
        def __str__(self) -> str:
            return "THING"

    out = resp._normalize_payload(Thing())
    assert out == {"context": "THING"}


# ------------------------------------- _now() --------------------------------------


def test_now_returns_iso_like_string() -> None:
    s: str = resp._now()
    assert "T" in s  # ISO 8601-ish
    assert len(s) >= 10


# -------------------------------- success_response() --------------------------------


def test_success_response_envelope() -> None:
    r = resp.success_response(data={"passed": 3}, message="ok", payload={"k": "v"})
    body = _json_of(r)
    assert r.status_code == 200
    assert body["success"] is True
    assert body["message"] == "ok"
    assert body["data"] == {"passed": 3}
    assert body["metadata"] == {"k": "v"}
    assert "timestamp" in body


# --------------------------------- error_response() ---------------------------------


def test_error_response_includes_traceback_when_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    # Force traceback on
    monkeypatch.setattr(resp, "_INCLUDE_TRACEBACK", True, raising=True)

    try:
        raise RuntimeError("boom")
    except RuntimeError:
        r = resp.error_response(status_code=418, message="fail", payload={"ctx": 1})

    body = _json_of(r)
    assert r.status_code == 418
    assert body["success"] is False
    assert body["message"] == "fail"
    assert body["data"] is None
    assert body["metadata"] == {"ctx": 1}
    assert "timestamp" in body
    # Traceback captured from the except context; must contain the exception string
    assert isinstance(body.get("traceback"), str)
    assert "RuntimeError: boom" in body["traceback"]


def test_error_response_omits_traceback_when_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    # Force traceback off
    monkeypatch.setattr(resp, "_INCLUDE_TRACEBACK", False, raising=True)
    r = resp.error_response(status_code=400, message="no tb", payload=None)
    body = _json_of(r)
    assert "traceback" not in body
    assert body["metadata"] == {}


# ------------------------ format_pytest_summary_tail() ------------------------


def test_format_pytest_summary_tail_various_cases() -> None:
    # Normal case: include failed/errors and keep zero for collected
    s1: dict[str, Any] = {"failed": 1, "errors": 0, "collected": 5, "xpassed": 0}
    tail1: str = resp.format_pytest_summary_tail(s1)
    # Must contain the keys in default order and include 0 for context
    assert "failed=1" in tail1
    assert "errors=0" in tail1
    assert "collected=5" in tail1
    # Keys not in default list ("xpassed") aren’t shown

    # Nothing to include
    s2: dict[str, Any] = {}
    assert resp.format_pytest_summary_tail(s2) == ""

    # Non-dict input
    assert resp.format_pytest_summary_tail(None) == ""
    assert resp.format_pytest_summary_tail("nope") == ""


def test_format_pytest_summary_tail_custom_keys() -> None:
    s: dict[str, Any] = {"warnings": 2, "xfailed": 1}
    tail: str = resp.format_pytest_summary_tail(s, keys=("warnings", "xfailed"))
    assert tail.strip().startswith("(") and "warnings=2" in tail and "xfailed=1" in tail


# ------------------------------- is_pytest_ok() -------------------------------


def test_is_pytest_ok_true_and_false_and_bad_inputs() -> None:
    assert resp.is_pytest_ok({"success": True, "exit_code": 0}) is True
    assert resp.is_pytest_ok({"success": True, "exit_code": 1}) is False
    assert resp.is_pytest_ok({"success": False, "exit_code": 0}) is False
    # Bad/edge inputs
    assert resp.is_pytest_ok({}) is False
    assert resp.is_pytest_ok({"success": "yes", "exit_code": "0"}) is False
    assert resp.is_pytest_ok({"success": True, "exit_code": "bogus"}) is False
