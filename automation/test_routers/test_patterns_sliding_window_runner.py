from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import patterns_sliding_window_runner as sw


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app: FastAPI = FastAPI()
    app.include_router(sw.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tags, and path."""
    routes: set[str] = {r.path for r in app.router.routes}
    assert "/patterns/sliding-window/submit" in routes
    assert sw.router.prefix == "/patterns/sliding-window"
    assert any("Patterns - Sliding Window Practice" in t for t in sw.router.tags)


@pytest.mark.asyncio
async def test_submit_sliding_window_practice_invokes_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The route function should await the generated handler and return its result."""
    called: dict[str, object] = {}

    async def fake_submit(payload: object) -> dict:
        called["payload"] = payload
        return {"ok": True, "pattern": "sliding-window"}

    monkeypatch.setattr(sw, "_submit", fake_submit)

    payload: object = type("Dummy", (), {"methods": {"max_sum": "def max_sum(a, k): pass"}})()
    result: dict = await sw.submit_sliding_window_practice(payload)  # type: ignore[arg-type]

    assert called["payload"] is payload
    assert result == {"ok": True, "pattern": "sliding-window"}


def test_submit_sliding_window_practice_through_http(
    app: FastAPI, monkeypatch: pytest.MonkeyPatch
) -> None:
    """End-to-end HTTP check to ensure route wiring works."""
    client: TestClient = TestClient(app)

    async def fake_submit(payload: object) -> dict:
        return {"ok": True}

    monkeypatch.setattr(sw, "_submit", fake_submit)

    resp = client.post(
        "/patterns/sliding-window/submit",
        json={"methods": {"max_sum": "def max_sum(a, k): pass"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
