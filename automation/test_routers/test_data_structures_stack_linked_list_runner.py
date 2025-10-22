from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import data_structures_stack_linked_list_runner as sll


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app: FastAPI = FastAPI()
    app.include_router(sll.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tags, and path."""
    routes: set[str] = {r.path for r in app.router.routes}
    assert "/data-structures/stack/linked-list/submit" in routes
    assert sll.router.prefix == "/data-structures/stack/linked-list"
    assert any("Data Structures - Stack (Linked List) Practice" in t for t in sll.router.tags)


@pytest.mark.asyncio
async def test_submit_stack_linked_list_practice_invokes_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The route function should await the generated handler and return its result."""
    called: dict[str, object] = {}

    async def fake_submit(payload: object) -> dict:
        called["payload"] = payload
        return {"ok": True, "kind": "stack-linked-list"}

    monkeypatch.setattr(sll, "_submit", fake_submit)

    payload: object = type("Dummy", (), {"methods": {"push": "def push(x): pass"}})()
    result: dict = await sll.submit_stack_linked_list_practice(payload)  # type: ignore[arg-type]

    assert called["payload"] is payload
    assert result == {"ok": True, "kind": "stack-linked-list"}


def test_submit_stack_linked_list_practice_through_http(
    app: FastAPI, monkeypatch: pytest.MonkeyPatch
) -> None:
    """End-to-end HTTP check to ensure route wiring works."""
    client: TestClient = TestClient(app)

    async def fake_submit(payload: object) -> dict:
        return {"ok": True}

    monkeypatch.setattr(sll, "_submit", fake_submit)

    resp = client.post(
        "/data-structures/stack/linked-list/submit",
        json={"methods": {"push": "def push(x): pass"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
