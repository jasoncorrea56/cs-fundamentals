from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import data_structures_queue_array_router as qa


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app: FastAPI = FastAPI()
    app.include_router(qa.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tags, and path."""
    routes: set[str] = {r.path for r in app.router.routes}
    assert "/data-structures/queue/array/submit" in routes
    assert qa.router.prefix == "/data-structures/queue/array"
    assert any("Data Structures - Queue (Circular Array) Practice" in t for t in qa.router.tags)


@pytest.mark.asyncio
async def test_submit_queue_array_practice_invokes_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The route function should await the generated handler and return its result."""
    called: dict[str, object] = {}

    async def fake_submit(payload: object) -> dict:
        called["payload"] = payload
        return {"ok": True, "kind": "queue-array"}

    monkeypatch.setattr(qa, "_submit", fake_submit)

    payload: object = type("Dummy", (), {"methods": {"enqueue": "def enqueue(x): pass"}})()
    result: dict = await qa.submit_queue_array_practice(payload)  # type: ignore[arg-type]

    assert called["payload"] is payload
    assert result == {"ok": True, "kind": "queue-array"}


def test_submit_queue_array_practice_through_http(
    app: FastAPI, monkeypatch: pytest.MonkeyPatch
) -> None:
    """End-to-end HTTP check to ensure route wiring works."""
    client: TestClient = TestClient(app)

    async def fake_submit(payload: object) -> dict:
        return {"ok": True}

    monkeypatch.setattr(qa, "_submit", fake_submit)

    resp = client.post(
        "/data-structures/queue/array/submit",
        json={"methods": {"enqueue": "def enqueue(x): pass"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
