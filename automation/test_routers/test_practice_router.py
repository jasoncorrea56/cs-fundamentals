from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.models.schemas import PracticeSubmission
from cs_fundamentals.routers import practice_router as pr
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


# ---------- App fixture --------------------------------------------------------


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app: FastAPI = FastAPI()
    app.include_router(pr.router)
    return app


# ---------- Router wiring ------------------------------------------------------


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tag, and path."""
    routes: set[str] = {r.path for r in app.router.routes}
    assert "/practice/submit" in routes
    assert pr.router.prefix == "/practice"
    assert any("Practice Runner" in t for t in pr.router.tags)


# ---------- Success path -------------------------------------------------------


@pytest.mark.asyncio
async def test_submit_practice_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """When tests pass, return 200 with standardized success envelope and payload metadata."""
    payload: PracticeSubmission = PracticeSubmission(
        module="m.mod",
        class_name="PracticeCls",
        methods={"f": "def f(): pass"},
        test_files=["automation/tests/test_x.py"],
        test_expr="x and y",
    )

    fake_result: dict[str, Any] = {"success": True, "exit_code": 0, "summary": {"passed": 1}}
    monkeypatch.setattr(pr, "run_submission", lambda **kw: fake_result)
    monkeypatch.setattr(pr, "is_pytest_ok", lambda result: True)

    resp = await pr.submit_practice(payload)

    import json as _json

    content: dict[str, Any] = _json.loads(resp.body.decode())

    assert resp.status_code == 200
    assert content["success"] is True
    assert content["message"] == "All tests executed successfully."
    assert content["data"] == fake_result
    # metadata should be payload.model_dump()
    assert content["metadata"] == payload.model_dump()


def test_submit_practice_success_http(app: FastAPI, monkeypatch: pytest.MonkeyPatch) -> None:
    """HTTP E2E for success."""
    client: TestClient = TestClient(app)
    fake_result: dict[str, Any] = {"success": True, "exit_code": 0, "summary": {"passed": 2}}
    monkeypatch.setattr(pr, "run_submission", lambda **kw: fake_result)
    monkeypatch.setattr(pr, "is_pytest_ok", lambda result: True)

    resp = client.post(
        "/practice/submit",
        json={
            "module": "m.mod",
            "class_name": "PracticeCls",
            "methods": {"f": "def f(): pass"},
            "test_files": ["automation/tests/test_x.py"],
            "test_expr": "x and y",
        },
    )
    assert resp.status_code == 200
    j = resp.json()
    assert j["success"] is True
    assert j["data"] == fake_result
    assert j["metadata"]["module"] == "m.mod"
    assert j["metadata"]["class_name"] == "PracticeCls"


# ---------- Failure path (pytest failures) ------------------------------------


@pytest.mark.asyncio
async def test_submit_practice_test_failures(monkeypatch: pytest.MonkeyPatch) -> None:
    """When tests fail, return 400 with formatted summary tail and combined payload."""
    payload: PracticeSubmission = PracticeSubmission(
        module="m.mod",
        class_name="PracticeCls",
        methods={"f": "def f(): pass"},
        test_files=None,
        test_expr=None,
    )
    fake_result: dict[str, Any] = {
        "success": False,
        "exit_code": 1,
        "summary": {"failed": 1, "collected": 3},
    }

    monkeypatch.setattr(pr, "run_submission", lambda **kw: fake_result)
    monkeypatch.setattr(pr, "is_pytest_ok", lambda result: False)
    monkeypatch.setattr(pr, "format_pytest_summary_tail", lambda s: " (failed=1, collected=3)")

    resp = await pr.submit_practice(payload)
    import json as _json

    content: dict[str, Any] = _json.loads(resp.body.decode())

    assert resp.status_code == 400
    assert content["success"] is False
    # message should include our formatted tail
    assert "Test run failed (failed=1, collected=3)" in content["message"]
    # payload/metadata should include both submission and result
    md: dict[str, Any] = content["metadata"]
    assert "submission" in md and "result" in md
    assert md["submission"] == payload.model_dump()
    assert md["result"] == fake_result


def test_submit_practice_test_failures_http(app: FastAPI, monkeypatch: pytest.MonkeyPatch) -> None:
    """HTTP E2E when tests fail."""
    client: TestClient = TestClient(app)
    fake_result: dict[str, Any] = {
        "success": False,
        "exit_code": 1,
        "summary": {"failed": 2, "collected": 5},
    }

    monkeypatch.setattr(pr, "run_submission", lambda **kw: fake_result)
    monkeypatch.setattr(pr, "is_pytest_ok", lambda result: False)
    monkeypatch.setattr(pr, "format_pytest_summary_tail", lambda s: " (failed=2, collected=5)")

    resp = client.post(
        "/practice/submit",
        json={"module": "m.mod", "class_name": "PracticeCls", "methods": {"f": "def f(): pass"}},
    )
    assert resp.status_code == 400
    j = resp.json()
    assert j["success"] is False
    assert "failed=2" in j["message"]


# ---------- Disallowed import handling ----------------------------------------


@pytest.mark.asyncio
async def test_submit_practice_disallowed_import(monkeypatch: pytest.MonkeyPatch) -> None:
    """Disallowed imports should yield a 400 envelope with error message."""
    payload: PracticeSubmission = PracticeSubmission(
        module="m.mod",
        class_name="PracticeCls",
        methods={"f": "def f(): pass"},
        test_files=None,
        test_expr=None,
    )

    def boom(**kw: Any) -> dict[str, Any]:
        raise pr.DisallowedImportError("Import of 'os' is not allowed")

    monkeypatch.setattr(pr, "run_submission", boom)

    resp = await pr.submit_practice(payload)
    import json as _json

    content: dict[str, Any] = _json.loads(resp.body.decode())

    assert resp.status_code == 400
    assert content["success"] is False
    assert "Import of 'os' is not allowed" in content["message"]
    # metadata is the original submission
    assert content["metadata"] == payload.model_dump()


# ---------- Generic exception handling ----------------------------------------


@pytest.mark.asyncio
async def test_submit_practice_generic_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unexpected exceptions should be wrapped into 400 error envelopes, with traceback included by helper."""
    payload: PracticeSubmission = PracticeSubmission(
        module="m.mod",
        class_name="PracticeCls",
        methods={"f": "def f(): pass"},
        test_files=None,
        test_expr=None,
    )

    def kaboom(**kw: Any) -> dict[str, Any]:
        raise RuntimeError("boom")

    monkeypatch.setattr(pr, "run_submission", kaboom)

    resp = await pr.submit_practice(payload)
    import json as _json

    content: dict[str, Any] = _json.loads(resp.body.decode())

    assert resp.status_code == 400
    assert content["success"] is False
    assert "boom" in content["message"]
    # Always includes metadata of the original submission
    assert content["metadata"] == payload.model_dump()
    # Optionally a "traceback" key exists (controlled by PRACTICE_INCLUDE_TRACEBACK)
    # We don't assert presence to avoid coupling to env, but if present it must be a string.
    if "traceback" in content:
        assert isinstance(content["traceback"], str)


# ---------- Basic model validation --------------------------------------------


def test_practice_submission_model_validation() -> None:
    """Quick sanity check for the incoming model used by the router."""
    with pytest.raises(Exception):
        PracticeSubmission()  # type: ignore[call-arg]

    ps = PracticeSubmission(module="m", class_name="C", methods={"f": "def f(): pass"})
    assert ps.module == "m"
    assert ps.class_name == "C"
    assert "f" in ps.methods
