from __future__ import annotations

from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import data_structures_bst_router as bst


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app = FastAPI()
    app.include_router(bst.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should have expected prefix and tags."""
    routes = {r.path for r in app.router.routes}
    assert "/data-structures/bst/submit" in routes
    assert any("Data Structures - Binary Search Tree Practice" in t for t in bst.router.tags)
    assert bst.router.prefix == "/data-structures/bst"


@pytest.mark.asyncio
async def test_submit_bst_practice_invokes_factory(monkeypatch: pytest.MonkeyPatch) -> None:
    """submit_bst_practice should await the generated handler and return its result."""
    called: dict[str, object] = {}

    async def fake_submit(payload) -> dict[str, Any]:
        called["payload"] = payload
        return {"ok": True, "echo": payload.methods}

    # Patch the generated handler
    monkeypatch.setattr(bst, "_submit", fake_submit)

    payload = type("Dummy", (), {"methods": {"foo": "bar"}})()
    result = await bst.submit_bst_practice(payload)

    assert called["payload"] is payload
    assert result == {"ok": True, "echo": {"foo": "bar"}}


def test_submit_bst_practice_through_http(app: FastAPI, monkeypatch: pytest.MonkeyPatch) -> None:
    """End-to-end check via TestClient to ensure route wiring works."""
    client: TestClient = TestClient(app)

    async def fake_submit(payload: object) -> dict:
        return {"ok": True}

    monkeypatch.setattr(bst, "_submit", fake_submit)

    resp = client.post(
        "/data-structures/bst/submit",
        json={"methods": {"a": "def a(): pass"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
