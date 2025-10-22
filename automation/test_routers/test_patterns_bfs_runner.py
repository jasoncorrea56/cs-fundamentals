from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import patterns_bfs_runner as bfs


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app: FastAPI = FastAPI()
    app.include_router(bfs.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tags, and path."""
    routes: set[str] = {r.path for r in app.router.routes}
    assert "/patterns/bfs/submit" in routes
    assert bfs.router.prefix == "/patterns/bfs"
    assert any("Patterns - Breadth First Search Practice" in t for t in bfs.router.tags)


@pytest.mark.asyncio
async def test_submit_bfs_practice_invokes_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The route function should await the generated handler and return its result."""
    called: dict[str, object] = {}

    async def fake_submit(payload: object) -> dict:
        called["payload"] = payload
        return {"ok": True, "pattern": "bfs"}

    monkeypatch.setattr(bfs, "_submit", fake_submit)

    payload: object = type(
        "Dummy", (), {"methods": {"level_order": "def level_order(root): pass"}}
    )()
    result: dict = await bfs.submit_bfs_practice(payload)  # type: ignore[arg-type]

    assert called["payload"] is payload
    assert result == {"ok": True, "pattern": "bfs"}


def test_submit_bfs_practice_through_http(app: FastAPI, monkeypatch: pytest.MonkeyPatch) -> None:
    """End-to-end HTTP check to ensure route wiring works."""
    client: TestClient = TestClient(app)

    async def fake_submit(payload: object) -> dict:
        return {"ok": True}

    monkeypatch.setattr(bfs, "_submit", fake_submit)

    resp = client.post(
        "/patterns/bfs/submit",
        json={"methods": {"level_order": "def level_order(root): pass"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
