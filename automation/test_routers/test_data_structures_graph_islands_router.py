from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import data_structures_graph_islands_router as gi


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app = FastAPI()
    app.include_router(gi.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tags, and path."""
    routes = {r.path for r in app.router.routes}
    assert "/data-structures/graph/islands/submit" in routes
    assert gi.router.prefix == "/data-structures/graph/islands"
    assert any("Data Structures - Graph (Islands II) Practice" in t for t in gi.router.tags)


def test_split_union_find_splits_primary_and_inner() -> None:
    """Splitter should route UnionFind.* keys into the nested injection tuple."""
    methods: dict[str, str] = {
        "solve": "def solve(): pass",
        "UnionFind.find": "def find(x): pass",
        "UnionFind.union": "def union(x, y): pass",
        "helper": "def helper(): pass",
    }
    primary, extra = gi._split_union_find(methods)

    # Primary should contain non-UnionFind methods
    assert set(primary.keys()) == {"solve", "helper"}

    # Extra should contain one 3-tuple: (module, class_name, inner_methods)
    assert isinstance(extra, list) and len(extra) == 1
    tup = extra[0]
    # Defensive shape checks because the module’s annotation is loose
    assert isinstance(tup, tuple) and len(tup) == 3
    mod, cls, inner = tup  # type: ignore[misc]
    assert mod == "cs_fundamentals.data_structures.graph"
    assert cls == "PracticeGraphProblems.UnionFind"
    assert set(inner.keys()) == {"find", "union"}


def test_split_union_find_when_no_inner_methods() -> None:
    """Splitter should return an empty extra list when no UnionFind.* keys are present."""
    methods: dict[str, str] = {"a": "def a(): pass", "b": "def b(): pass"}
    primary, extra = gi._split_union_find(methods)
    assert set(primary.keys()) == {"a", "b"}
    assert extra == []


@pytest.mark.asyncio
async def test_submit_graph_islands_practice_invokes_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The route function should await the generated handler and return its result."""
    called: dict[str, object] = {}

    async def fake_submit(payload: object) -> dict:
        called["payload"] = payload
        return {"ok": True, "kind": "graph-islands"}

    monkeypatch.setattr(gi, "_submit", fake_submit)

    payload = type("Dummy", (), {"methods": {"solve": "def solve(): pass"}})()
    result = await gi.submit_graph_islands_practice(payload)

    assert called["payload"] is payload
    assert result == {"ok": True, "kind": "graph-islands"}


def test_submit_graph_islands_practice_through_http(
    app: FastAPI, monkeypatch: pytest.MonkeyPatch
) -> None:
    """End-to-end HTTP check to ensure route wiring works."""
    client = TestClient(app)

    async def fake_submit(payload: object) -> dict:
        return {"ok": True}

    monkeypatch.setattr(gi, "_submit", fake_submit)

    resp = client.post(
        "/data-structures/graph/islands/submit",
        json={"methods": {"solve": "def solve(): pass", "UnionFind.find": "def find(x): pass"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
