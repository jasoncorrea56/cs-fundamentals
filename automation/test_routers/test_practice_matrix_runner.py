from __future__ import annotations

from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import practice_matrix_runner as pm


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app: FastAPI = FastAPI()
    app.include_router(pm.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tags, and path."""
    routes: set[str] = {r.path for r in app.router.routes}
    assert "/practice-matrix/submit" in routes
    assert pm.router.prefix == "/practice-matrix"
    assert any("Practice Runner (Matrix)" in t for t in pm.router.tags)


@pytest.mark.asyncio
async def test_submit_via_matrix_invokes_handler_with_shim(monkeypatch: pytest.MonkeyPatch) -> None:
    """submit_via_matrix should fetch a handler and pass only the 'methods' via the shim model."""
    captured: dict[str, object] = {}

    async def fake_handler(shim_payload: object) -> dict[str, Any]:
        # The shim is a Pydantic model with 'methods' field; we only care that it carries the methods through.
        captured["shim_type"] = type(shim_payload).__name__
        captured["methods"] = getattr(shim_payload, "methods", None)
        return {"ok": True, "from_key": captured.get("key")}

    def fake_factory(
        *, key: str, success_message: str | None = None, method_splitter=None
    ) -> dict[str, Any]:
        captured["key"] = key
        captured["success_message"] = success_message
        captured["method_splitter"] = method_splitter
        return fake_handler

    monkeypatch.setattr(pm, "make_submit_handler_from_matrix", fake_factory)

    payload: pm.MatrixSubmission = pm.MatrixSubmission(
        key="patterns.dfs",
        methods={"preorder": "def preorder(root): pass"},
    )
    result: dict = await pm.submit_via_matrix(payload)
    assert result == {"ok": True, "from_key": "patterns.dfs"}
    assert captured["shim_type"] == "_Shim"
    assert captured["methods"] == {"preorder": "def preorder(root): pass"}


def test_submit_via_matrix_through_http(app: FastAPI, monkeypatch: pytest.MonkeyPatch) -> None:
    """End-to-end HTTP check to ensure route wiring works and shim is applied."""
    client: TestClient = TestClient(app)

    async def fake_handler(shim_payload: object) -> dict[str, Any]:
        return {"ok": True, "methods": getattr(shim_payload, "methods", None)}

    def fake_factory(
        *, key: str, success_message: str | None = None, method_splitter=None
    ) -> dict[str, Any]:
        # Assert key plumbing happens here.
        assert key == "patterns.bfs"
        return fake_handler

    monkeypatch.setattr(pm, "make_submit_handler_from_matrix", fake_factory)

    resp = client.post(
        "/practice-matrix/submit",
        json={
            "key": "patterns.bfs",
            "methods": {"level_order": "def level_order(root): pass"},
        },
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True, "methods": {"level_order": "def level_order(root): pass"}}


def test_matrix_submission_model_validation() -> None:
    """Pydantic model should require 'key' and 'methods' and store example metadata."""
    with pytest.raises(Exception):
        pm.MatrixSubmission()  # type: ignore[call-arg]

    ms: pm.MatrixSubmission = pm.MatrixSubmission(
        key="patterns.bfs", methods={"m": "def m(): pass"}
    )
    assert ms.key == "patterns.bfs"
    assert ms.methods == {"m": "def m(): pass"}

    # Example metadata is defined on the 'key' field.
    key_field = pm.MatrixSubmission.model_fields["key"]
    jse = getattr(key_field, "json_schema_extra", None)
    if isinstance(jse, dict):
        assert jse.get("example") == "patterns.dfs"
