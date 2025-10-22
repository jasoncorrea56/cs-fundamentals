from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import data_structures_min_heap_runner as mn


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app: FastAPI = FastAPI()
    app.include_router(mn.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tags, and path."""
    routes: set[str] = {r.path for r in app.router.routes}
    assert "/data-structures/min-heap/submit" in routes
    assert mn.router.prefix == "/data-structures/min-heap"
    # Tag string should contain "MinHeap Practice" per router definition.
    assert any("Data Structures - MinHeap Practice" in t for t in mn.router.tags)


@pytest.mark.asyncio
async def test_submit_min_heap_practice_invokes_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The route function should await the generated handler and return its result."""
    called: dict[str, object] = {}

    async def fake_submit(payload: object) -> dict:
        called["payload"] = payload
        return {"ok": True, "kind": "min-heap"}

    monkeypatch.setattr(mn, "_submit", fake_submit)

    payload: object = type("Dummy", (), {"methods": {"push": "def push(x): pass"}})()
    submit_fn = getattr(mn, "submit_min_heap_practice")
    result: dict = await submit_fn(payload)  # type: ignore[no-untyped-call]

    assert called["payload"] is payload
    assert result == {"ok": True, "kind": "min-heap"}


def test_submit_min_heap_practice_through_http(
    app: FastAPI, monkeypatch: pytest.MonkeyPatch
) -> None:
    """End-to-end HTTP check to ensure route wiring works."""
    client: TestClient = TestClient(app)

    async def fake_submit(payload: object) -> dict:
        return {"ok": True}

    monkeypatch.setattr(mn, "_submit", fake_submit)

    resp = client.post(
        "/data-structures/min-heap/submit",
        json={"methods": {"push": "def push(x): pass"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
