from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import data_structures_linked_list_single_runner as lls


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app = FastAPI()
    app.include_router(lls.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tags, and path."""
    routes = {r.path for r in app.router.routes}
    assert "/data-structures/linked-list-single/submit" in routes
    assert lls.router.prefix == "/data-structures/linked-list-single"
    assert any("Data Structures - Singly Linked List Practice" in t for t in lls.router.tags)


@pytest.mark.asyncio
async def test_submit_single_linked_list_practice_invokes_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The route function should await the generated handler and return its result."""
    called: dict[str, object] = {}

    async def fake_submit(payload: object) -> dict:
        called["payload"] = payload
        return {"ok": True, "kind": "sll"}

    monkeypatch.setattr(lls, "_submit", fake_submit)

    payload = type("Dummy", (), {"methods": {"append": "def append(x): pass"}})()
    result = await lls.submit_single_linked_list_practice(payload)

    assert called["payload"] is payload
    assert result == {"ok": True, "kind": "sll"}


def test_submit_single_linked_list_practice_through_http(
    app: FastAPI, monkeypatch: pytest.MonkeyPatch
) -> None:
    """End-to-end HTTP check to ensure route wiring works."""
    client = TestClient(app)

    async def fake_submit(payload: object) -> dict:
        return {"ok": True}

    monkeypatch.setattr(lls, "_submit", fake_submit)

    resp = client.post(
        "/data-structures/linked-list-single/submit",
        json={"methods": {"append": "def append(x): pass"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
