from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import patterns_two_pointers_router as tp


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app: FastAPI = FastAPI()
    app.include_router(tp.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tags, and path."""
    routes: set[str] = {r.path for r in app.router.routes}
    assert "/patterns/two-pointers/submit" in routes
    assert tp.router.prefix == "/patterns/two-pointers"
    assert any("Patterns - Two Pointers Practice" in t for t in tp.router.tags)


@pytest.mark.asyncio
async def test_submit_two_pointers_practice_invokes_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The route function should await the generated handler and return its result."""
    called: dict[str, object] = {}

    async def fake_submit(payload: object) -> dict:
        called["payload"] = payload
        return {"ok": True, "pattern": "two-pointers"}

    monkeypatch.setattr(tp, "_submit", fake_submit)

    payload: object = type("Dummy", (), {"methods": {"two_sum": "def two_sum(nums): pass"}})()
    result: dict = await tp.submit_two_pointers_practice(payload)  # type: ignore[arg-type]

    assert called["payload"] is payload
    assert result == {"ok": True, "pattern": "two-pointers"}


def test_submit_two_pointers_practice_through_http(
    app: FastAPI, monkeypatch: pytest.MonkeyPatch
) -> None:
    """End-to-end HTTP check to ensure route wiring works."""
    client: TestClient = TestClient(app)

    async def fake_submit(payload: object) -> dict:
        return {"ok": True}

    monkeypatch.setattr(tp, "_submit", fake_submit)

    resp = client.post(
        "/patterns/two-pointers/submit",
        json={"methods": {"two_sum": "def two_sum(nums): pass"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
