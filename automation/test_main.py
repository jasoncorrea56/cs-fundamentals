from __future__ import annotations

import importlib
import sys
from typing import Any, cast, TYPE_CHECKING

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import cs_fundamentals.config as cfg
import cs_fundamentals.core.utility as util

if TYPE_CHECKING:
    from collections.abc import Iterable
    from fastapi import FastAPI
    from starlette.middleware import Middleware


def _reload_main_with(
    monkeypatch: pytest.MonkeyPatch,
    *,
    app_name: str = "Test App",
    version: str = "9.9.9",
) -> Any:
    """
    Reload cs_fundamentals.main after monkeypatching dependencies so the
    FastAPI app is built with deterministic title/version.
    """
    # Ensure a fresh Settings instance and set app_name deterministically
    clean_settings = cfg.Settings(_env_file=None)
    clean_settings.app_name = app_name  # type: ignore[assignment]
    monkeypatch.setattr(cfg, "settings", clean_settings, raising=True)

    # Freeze app version
    monkeypatch.setattr(util, "get_app_version", lambda: version, raising=True)

    # Reload main so it re-reads settings/get_app_version and rebuilds app
    sys.modules.pop("cs_fundamentals.main", None)
    main = importlib.import_module("cs_fundamentals.main")
    return main


@pytest.fixture()
def main_module(monkeypatch: pytest.MonkeyPatch) -> Any:
    """Provide a freshly reloaded main module with deterministic config."""
    return _reload_main_with(monkeypatch, app_name="Test App", version="9.9.9")


def test_app_title_and_version(main_module: Any) -> None:
    app: FastAPI = cast("FastAPI", main_module.app)
    assert app.title == "Test App"
    assert app.version == "9.9.9"


def test_root_endpoint_and_docs_link(main_module: Any) -> None:
    app: FastAPI = main_module.app
    client: TestClient = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    payload: dict[str, str] = r.json()
    assert payload["message"] == "API is running"
    assert payload["docs"] == "/docs"


def test_some_routes_are_mounted(main_module: Any) -> None:
    """Spot-check a couple of routers to ensure they’re included."""
    app: FastAPI = main_module.app
    client: TestClient = TestClient(app)

    # Health routes
    r1 = client.get("/api/v1/healthz")
    assert r1.status_code == 200
    assert r1.json() == {"status": "ok"}

    # Targets route
    r2 = client.get("/api/v1/targets")
    assert r2.status_code == 200
    assert isinstance(r2.json(), list)


def test_middleware_stack_contains_expected_classes(main_module: Any) -> None:
    """
    Verify middleware classes and addition order.
    FastAPI stores user_middleware in the order added; Starlette reverses it on build.
    """
    app: FastAPI = main_module.app
    user_mw: Iterable[Middleware] = app.user_middleware

    cls_list = [mw.cls for mw in user_mw]
    # Expect RequestLoggerMiddleware added first, XRequestIDMiddleware added second
    from cs_fundamentals.api.middleware import (
        RequestLoggerMiddleware,
        XRequestIDMiddleware,
    )

    assert RequestLoggerMiddleware in cls_list
    assert XRequestIDMiddleware in cls_list

    # Added order as recorded by FastAPI (user_middleware lists inner before outer)
    idx_x: int = cls_list.index(XRequestIDMiddleware)
    idx_req: int = cls_list.index(RequestLoggerMiddleware)
    assert idx_x < idx_req


def test_lifespan_logs_startup_and_shutdown(
    main_module: Any, caplog: pytest.LogCaptureFixture
) -> None:
    """
    Enter/exit TestClient context to trigger lifespan; assert logs present.
    """
    app: FastAPI = main_module.app
    with TestClient(app) as _client:
        pass

    text: str = caplog.text
    assert "event=api.lifespan.startup" in text
    assert "event=api.lifespan.shutdown" in text


def test_x_request_id_header_present(main_module: Any) -> None:
    """
    Simple smoke: X-Request-ID middleware sets a header on responses.
    """
    app: FastAPI = main_module.app
    client: TestClient = TestClient(app)
    r = client.get("/api/v1/healthz", headers={"X-Request-ID": "abc123"})
    assert r.status_code == 200
    assert r.headers.get("X-Request-ID") == "abc123"
