from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import data_structures_queue_linked_list_router as qll


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app: FastAPI = FastAPI()
    app.include_router(qll.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tags, and path."""
    routes: set[str] = {r.path for r in app.router.routes}
    assert "/data-structures/queue/linked-list/submit" in routes
    assert qll.router.prefix == "/data-structures/queue/linked-list"
    assert any(
        "Data Structures - Queue (Circular Linked List) Practice" in t for t in qll.router.tags
    )


@pytest.mark.asyncio
async def test_submit_queue_linked_list_practice_invokes_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The route function should await the generated handler and return its result."""
    called: dict[str, object] = {}

    async def fake_submit(payload: object) -> dict:
        called["payload"] = payload
        return {"ok": True, "kind": "queue-linked-list"}

    monkeypatch.setattr(qll, "_submit", fake_submit)

    payload: object = type("Dummy", (), {"methods": {"enqueue": "def enqueue(x): pass"}})()
    result: dict = await qll.submit_queue_linked_list_practice(payload)  # type: ignore[arg-type]

    assert called["payload"] is payload
    assert result == {"ok": True, "kind": "queue-linked-list"}


def test_submit_queue_linked_list_practice_through_http(
    app: FastAPI, monkeypatch: pytest.MonkeyPatch
) -> None:
    """End-to-end HTTP check to ensure route wiring works."""
    client: TestClient = TestClient(app)

    async def fake_submit(payload: object) -> dict:
        return {"ok": True}

    monkeypatch.setattr(qll, "_submit", fake_submit)

    resp = client.post(
        "/data-structures/queue/linked-list/submit",
        json={"methods": {"enqueue": "def enqueue(x): pass"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
