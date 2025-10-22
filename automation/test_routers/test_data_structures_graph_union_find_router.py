from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import data_structures_graph_union_find_router as guf


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app = FastAPI()
    app.include_router(guf.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tags, and path."""
    routes = {r.path for r in app.router.routes}
    assert "/data-structures/graph/union-find/submit" in routes
    assert guf.router.prefix == "/data-structures/graph/union-find"
    assert any("Data Structures - Graph (Union-Find) Practice" in t for t in guf.router.tags)


@pytest.mark.asyncio
async def test_submit_graph_union_find_practice_invokes_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The route function should await the generated handler and return its result."""
    called: dict[str, object] = {}

    async def fake_submit(payload: object) -> dict:
        called["payload"] = payload
        return {"ok": True, "kind": "graph-union-find"}

    monkeypatch.setattr(guf, "_submit", fake_submit)

    payload = type("Dummy", (), {"methods": {"union": "def union(a,b): pass"}})()
    result = await guf.submit_graph_union_find_practice(payload)

    assert called["payload"] is payload
    assert result == {"ok": True, "kind": "graph-union-find"}


def test_submit_graph_union_find_practice_through_http(
    app: FastAPI, monkeypatch: pytest.MonkeyPatch
) -> None:
    """End-to-end HTTP check to ensure route wiring works."""
    client: TestClient = TestClient(app)

    async def fake_submit(payload: object) -> dict:
        return {"ok": True}

    monkeypatch.setattr(guf, "_submit", fake_submit)

    resp = client.post(
        "/data-structures/graph/union-find/submit",
        json={"methods": {"union": "def union(a,b): pass"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
