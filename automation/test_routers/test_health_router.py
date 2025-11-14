from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import health_router as hl


@pytest.fixture()
def app() -> FastAPI:
    """Mount the health router in a minimal FastAPI app."""
    app = FastAPI()
    app.include_router(hl.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should expose expected endpoints."""
    paths = {r.path for r in app.router.routes}
    assert "/configz" in paths
    assert "/healthz" in paths
    assert "/version" in paths
    assert "Health" in hl.router.tags


def test_configz_returns_expected_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure configz returns sanitized settings with boolean DB field."""
    dummy_settings = type(
        "DummySettings",
        (),
        {
            "env": "test",
            "log_level": "DEBUG",
            "port": 9999,
            "db_url": "postgresql://dummy/db",
        },
    )
    monkeypatch.setattr(hl, "settings", dummy_settings)
    result = hl.configz()

    assert result == {
        "env": "test",
        "log_level": "DEBUG",
        "port": 9999,
        "has_db_url": True,
    }


@pytest.mark.asyncio
async def test_healthz_returns_ok() -> None:
    """healthz endpoint should return a simple OK status."""
    result = await hl.healthz()
    assert result == {"status": "ok"}


def test_version_uses_get_app_version(monkeypatch: pytest.MonkeyPatch) -> None:
    """version() should return app name, image tag, and version from get_app_version()."""
    monkeypatch.setattr(hl, "get_app_version", lambda: "1.2.3")

    dummy_settings = type("DummySettings", (), {"app_name": "cs-fundamentals"})
    monkeypatch.setattr(hl, "settings", dummy_settings)

    # Ensure deterministic value for the env var
    monkeypatch.setenv("CSF_IMAGE_TAG", "0.6.9-dxrdbfe")

    result = hl.version()

    assert result == {
        "app": "cs-fundamentals",
        "image-tag": "0.6.9-dxrdbfe",
        "version": "1.2.3",
    }


def test_http_endpoints(app: FastAPI, monkeypatch: pytest.MonkeyPatch) -> None:
    """Validate all health endpoints through HTTP."""
    client = TestClient(app)

    # Mock get_app_version for predictable output
    monkeypatch.setattr(hl, "get_app_version", lambda: "9.9.9")

    # Mock settings
    monkeypatch.setattr(
        hl,
        "settings",
        type(
            "DummySettings",
            (),
            {"env": "t", "log_level": "INFO", "port": 80, "db_url": None, "app_name": "cs-f"},
        )(),
    )

    # Ensure deterministic image tag
    monkeypatch.setenv("CSF_IMAGE_TAG", "test-tag-123")

    # /configz
    r1 = client.get("/configz")
    assert r1.status_code == 200
    body = r1.json()
    assert body["env"] == "t"
    assert body["has_db_url"] is False

    # /healthz
    r2 = client.get("/healthz")
    assert r2.status_code == 200
    assert r2.json() == {"status": "ok"}

    # /version
    r3 = client.get("/version")
    assert r3.status_code == 200
    assert r3.json() == {
        "app": "cs-f",
        "image-tag": "test-tag-123",
        "version": "9.9.9",
    }
