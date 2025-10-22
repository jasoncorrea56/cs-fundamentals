from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import patterns_sorting_router as sort


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app: FastAPI = FastAPI()
    app.include_router(sort.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tags, and path."""
    routes: set[str] = {r.path for r in app.router.routes}
    assert "/patterns/sorting/submit" in routes
    assert sort.router.prefix == "/patterns/sorting"
    assert any("Patterns - Sorting Practice" in t for t in sort.router.tags)


@pytest.mark.asyncio
async def test_submit_sorting_practice_invokes_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The route function should await the generated handler and return its result."""
    called: dict[str, object] = {}

    async def fake_submit(payload: object) -> dict:
        called["payload"] = payload
        return {"ok": True, "pattern": "sorting"}

    monkeypatch.setattr(sort, "_submit", fake_submit)

    payload: object = type("Dummy", (), {"methods": {"quick_sort": "def quick_sort(a): pass"}})()
    result: dict = await sort.submit_sorting_practice(payload)  # type: ignore[arg-type]

    assert called["payload"] is payload
    assert result == {"ok": True, "pattern": "sorting"}


def test_submit_sorting_practice_through_http(
    app: FastAPI, monkeypatch: pytest.MonkeyPatch
) -> None:
    """End-to-end HTTP check to ensure route wiring works."""
    client: TestClient = TestClient(app)

    async def fake_submit(payload: object) -> dict:
        return {"ok": True}

    monkeypatch.setattr(sort, "_submit", fake_submit)

    resp = client.post(
        "/patterns/sorting/submit",
        json={"methods": {"quick_sort": "def quick_sort(a): pass"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
