from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any, TYPE_CHECKING

from cs_fundamentals.core import utility as util

if TYPE_CHECKING:
    import pytest


def test_get_app_version_package_installed(monkeypatch: pytest.MonkeyPatch) -> None:
    """Simulate importlib.metadata.version succeeding."""
    monkeypatch.setattr(util, "get_version", lambda pkg: "1.2.3")
    assert util.get_app_version() == "1.2.3"


def test_get_app_version_package_not_found_pyproject_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Simulate PackageNotFoundError then successful toml read."""
    # Patch get_version to raise PackageNotFoundError
    monkeypatch.setattr(
        util, "get_version", lambda pkg: (_ for _ in ()).throw(util.PackageNotFoundError())
    )

    # Create fake pyproject.toml with version
    proj_dir = tmp_path / "cs_fundamentals"
    proj_dir.mkdir()
    pyproj = proj_dir / "pyproject.toml"
    pyproj.write_text("[project]\nversion = '9.9.9'\n")

    # Point __file__ to our temp dir to simulate path resolution
    monkeypatch.setattr(util, "__file__", str(proj_dir / "core" / "utility.py"))
    monkeypatch.setattr(util, "tomllib", tomllib)

    result = util.get_app_version()
    assert result == "9.9.9"


def test_get_app_version_pyproject_missing_fallback_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Simulate missing pyproject.toml and fall back to env var."""
    monkeypatch.setattr(
        util, "get_version", lambda pkg: (_ for _ in ()).throw(util.PackageNotFoundError())
    )

    # Make tomllib.load raise
    def fake_load(f: Any) -> Any:
        raise FileNotFoundError("no toml")

    monkeypatch.setattr(util.tomllib, "load", fake_load)
    monkeypatch.setattr(util, "__file__", str(Path.cwd() / "core" / "utility.py"))
    monkeypatch.setenv("APP_VERSION", "1.0.0-env")

    assert util.get_app_version() == "1.0.0-env"


def test_get_app_version_all_fallbacks(monkeypatch: pytest.MonkeyPatch) -> None:
    """Simulate everything failing, expect 'dev'."""
    monkeypatch.setattr(
        util, "get_version", lambda pkg: (_ for _ in ()).throw(util.PackageNotFoundError())
    )
    monkeypatch.setattr(util.tomllib, "load", lambda f: (_ for _ in ()).throw(RuntimeError("boom")))
    monkeypatch.delenv("APP_VERSION", raising=False)
    monkeypatch.setattr(util, "__file__", str(Path.cwd() / "core" / "utility.py"))

    assert util.get_app_version() == "dev"
