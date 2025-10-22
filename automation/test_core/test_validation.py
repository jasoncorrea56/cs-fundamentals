from __future__ import annotations

import types

import pytest

from cs_fundamentals.core import validation as val


def test_validate_methods_exist_all_methods_present(monkeypatch: pytest.MonkeyPatch) -> None:
    """Should silently succeed when all provided methods exist."""
    dummy_cls = types.SimpleNamespace(a=lambda: None, b=lambda: None)
    dummy_mod = types.SimpleNamespace(Dummy=dummy_cls)
    monkeypatch.setattr(val.importlib, "import_module", lambda m: dummy_mod)

    # All methods exist → no error expected
    val.validate_methods_exist("dummy_mod", "Dummy", ["a", "b"])


def test_validate_methods_exist_raises_for_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Should raise AttributeError listing missing methods."""
    dummy_cls = types.SimpleNamespace(a=lambda: None)
    dummy_mod = types.SimpleNamespace(Dummy=dummy_cls)
    monkeypatch.setattr(val.importlib, "import_module", lambda m: dummy_mod)

    with pytest.raises(AttributeError) as e:
        val.validate_methods_exist("fake.module", "Dummy", ["a", "missing_one"])
    msg = str(e.value)
    assert "Unknown method(s) for fake.module.Dummy" in msg
    assert "missing_one" in msg


def test_validate_methods_exist_handles_empty_list(monkeypatch: pytest.MonkeyPatch) -> None:
    """Should return cleanly if no methods are given."""
    dummy_cls = types.SimpleNamespace()
    dummy_mod = types.SimpleNamespace(Dummy=dummy_cls)
    monkeypatch.setattr(val.importlib, "import_module", lambda m: dummy_mod)

    val.validate_methods_exist("whatever.module", "Dummy", [])
