from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import patterns_singleton_router as sg


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app: FastAPI = FastAPI()
    app.include_router(sg.router)
    return app


# ---------- Router wiring ------------------------------------------------------


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tags, and path."""
    routes: set[str] = {r.path for r in app.router.routes}
    assert "/patterns/singleton/submit" in routes
    assert sg.router.prefix == "/patterns/singleton"
    assert any("Patterns - Singleton Practice" in t for t in sg.router.tags)


# ---------- Splitter behavior --------------------------------------------------


def test_singleton_splitter_routes_primary_and_extras() -> None:
    """Namespaced methods should route to the correct classes; bare __new__ goes to PracticeSingletonClass."""
    methods: dict[str, str] = {
        # Primary class (explicit)
        "PracticeSingletonClass.__new__": "def __new__(cls): pass",
        "PracticeSingletonClass.foo": "def foo(self): pass",
        # Bare __new__ should also map to PracticeSingletonClass
        "__new__": "def __new__(cls): pass",
        # Children / Borg variants (extras)
        "PracticeSingletonChild.__new__": "def __new__(cls): pass",
        "PracticeBorgSingletonClass.__new__": "def __new__(cls, *a, **k): pass",
        "PracticeBorgSingletonChild.__new__": "def __new__(cls): pass",
        "PracticeBorgSingletonResetChild.__new__": "def __new__(cls): pass",
    }

    primary, extras = sg._singleton_splitter(methods)

    # Primary contains explicit primary methods AND the bare __new__
    assert set(primary.keys()) == {"__new__", "foo", "__new__"} or set(primary.keys()) == {
        "__new__",
        "foo",
    }

    # Extras should contain one tuple for each non-primary target, with expected shapes
    extra_map: dict[str, dict[str, str]] = {}
    for tup in extras:
        assert isinstance(tup, tuple) and len(tup) == 3
        mod, cls, inner = tup
        assert mod == "cs_fundamentals.patterns.singleton"
        assert isinstance(cls, str)
        assert isinstance(inner, dict)
        extra_map[cls] = inner

    assert set(extra_map.keys()) == {
        "PracticeSingletonChild",
        "PracticeBorgSingletonClass",
        "PracticeBorgSingletonChild",
        "PracticeBorgSingletonResetChild",
    }
    # Spot-check one
    assert "__new__" in extra_map["PracticeSingletonChild"]


def test_singleton_splitter_keeps_unknown_namespaced_in_primary() -> None:
    """Unknown namespaced keys should remain in primary for later validation to raise."""
    methods: dict[str, str] = {
        "UnknownSingleton.__new__": "def __new__(cls): pass",
        "PracticeSingletonClass.bar": "def bar(self): pass",
    }
    primary, extras = sg._singleton_splitter(methods)

    assert "UnknownSingleton.__new__" in primary
    assert "bar" in primary
    assert extras == []


# ---------- Async handler + HTTP path -----------------------------------------


@pytest.mark.asyncio
async def test_submit_singleton_practice_invokes_factory(monkeypatch: pytest.MonkeyPatch) -> None:
    """The route function should await the generated handler and return its result."""
    called: dict[str, object] = {}

    async def fake_submit(payload: object) -> dict:
        called["payload"] = payload
        return {"ok": True, "pattern": "singleton"}

    monkeypatch.setattr(sg, "_submit", fake_submit)

    payload: object = type(
        "Dummy", (), {"methods": {"PracticeSingletonClass.__new__": "def __new__(cls): pass"}}
    )()
    result: dict = await sg.submit_singleton_practice(payload)  # type: ignore[arg-type]

    assert called["payload"] is payload
    assert result == {"ok": True, "pattern": "singleton"}


def test_submit_singleton_practice_through_http(
    app: FastAPI, monkeypatch: pytest.MonkeyPatch
) -> None:
    """End-to-end HTTP check to ensure route wiring works."""
    client: TestClient = TestClient(app)

    async def fake_submit(payload: object) -> dict:
        return {"ok": True}

    monkeypatch.setattr(sg, "_submit", fake_submit)

    resp = client.post(
        "/patterns/singleton/submit",
        json={"methods": {"PracticeSingletonClass.__new__": "def __new__(cls): pass"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
