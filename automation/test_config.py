from __future__ import annotations

import importlib

import cs_fundamentals.config as cfg
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest
    from pathlib import Path


def _clear_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove env vars that Settings may read."""
    for var in (
        "APP_NAME",
        "ENV",
        "PORT",
        "LOG_LEVEL",
        "DB_URL",
        "WEB_CONCURRENCY",
        "GRACEFUL_TIMEOUT",
    ):
        monkeypatch.delenv(var, raising=False)


def test_settings_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Defaults should match class-level definitions (with env isolated)."""
    _clear_env(monkeypatch)
    s = cfg.Settings(_env_file=None)  # do not read any .env here
    assert s.app_name == "CS Fundamentals API"
    assert s.env == "prod"
    assert s.port == 8000
    assert s.log_level == "INFO"
    assert s.db_url is None
    assert s.web_concurrency is None
    assert s.graceful_timeout is None


def test_settings_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    """Environment variables should override defaults."""
    _clear_env(monkeypatch)
    monkeypatch.setenv("ENV", "dev")
    monkeypatch.setenv("PORT", "9090")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("DB_URL", "sqlite:///mem.db")
    s = cfg.Settings(_env_file=None)
    assert s.env == "dev"
    assert s.port == 9090
    assert s.log_level == "DEBUG"
    assert s.db_url == "sqlite:///mem.db"


def test_settings_env_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Should read values from a provided .env file."""
    _clear_env(monkeypatch)
    env_file = tmp_path / ".env"
    env_file.write_text("ENV=test\nPORT=1234\nLOG_LEVEL=TRACE\n")
    s = cfg.Settings(_env_file=env_file)
    assert s.env == "test"
    assert s.port == 1234
    assert s.log_level == "TRACE"


def test_global_settings_instance_is_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    """Reload the module with a clean env so the global `settings` is deterministic."""
    _clear_env(monkeypatch)
    import cs_fundamentals.config as cfg_mod

    importlib.reload(cfg_mod)
    s = cfg_mod.settings
    assert isinstance(s, cfg_mod.Settings)
    # At least one default to confirm it didn't read env/ .env:
    assert s.app_name == "CS Fundamentals API"
