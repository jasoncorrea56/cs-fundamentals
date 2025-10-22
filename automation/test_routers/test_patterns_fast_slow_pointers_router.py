from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import patterns_fast_slow_pointers_router as fsp


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app: FastAPI = FastAPI()
    app.include_router(fsp.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tags, and path."""
    routes: set[str] = {r.path for r in app.router.routes}
    assert "/patterns/fast-slow-pointers/submit" in routes
    assert fsp.router.prefix == "/patterns/fast-slow-pointers"
    assert any("Patterns - Fast/Slow Pointers Practice" in t for t in fsp.router.tags)


@pytest.mark.asyncio
async def test_submit_fast_slow_pointers_invokes_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The route function should await the generated handler and return its result."""
    called: dict[str, object] = {}

    async def fake_submit(payload: object) -> dict:
        called["payload"] = payload
        return {"ok": True, "pattern": "fast_slow_pointers"}

    monkeypatch.setattr(fsp, "_submit", fake_submit)

    payload: object = type("Dummy", (), {"methods": {"has_cycle": "def has_cycle(head): pass"}})()
    result: dict = await fsp.submit_fast_slow_pointers_practice(payload)  # type: ignore[arg-type]

    assert called["payload"] is payload
    assert result == {"ok": True, "pattern": "fast_slow_pointers"}


def test_submit_fast_slow_pointers_through_http(
    app: FastAPI, monkeypatch: pytest.MonkeyPatch
) -> None:
    """End-to-end HTTP check to ensure route wiring works."""
    client: TestClient = TestClient(app)

    async def fake_submit(payload: object) -> dict:
        return {"ok": True}

    monkeypatch.setattr(fsp, "_submit", fake_submit)

    resp = client.post(
        "/patterns/fast-slow-pointers/submit",
        json={"methods": {"has_cycle": "def has_cycle(head): pass"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
