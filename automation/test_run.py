from __future__ import annotations

import runpy
import sys
import importlib
import warnings
from types import SimpleNamespace
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    import pytest


warnings.filterwarnings("ignore", category=RuntimeWarning)


def test_run_entrypoint_invokes_uvicorn(monkeypatch: pytest.MonkeyPatch) -> None:
    """Execute run.py as __main__ and verify uvicorn.run() args, without runpy warnings."""
    called: dict[str, Any] = {}

    # Inject a temporary setup_logging symbol so the import in run.py succeeds.
    import cs_fundamentals.core.logging_config as lc

    monkeypatch.setattr(
        lc, "setup_logging", lambda name: {"version": 1, "handlers": []}, raising=False
    )

    # Stub uvicorn.run.
    def fake_run(*args: object, **kwargs: object) -> str:
        called["args"] = args
        called["kwargs"] = kwargs
        return "ok"

    monkeypatch.setitem(sys.modules, "uvicorn", SimpleNamespace(run=fake_run))

    # Import once (normal import, not as __main__).
    sys.modules.pop("cs_fundamentals.run", None)
    importlib.import_module("cs_fundamentals.run")

    # Remove the cached module before executing as __main__ to avoid the warning.
    sys.modules.pop("cs_fundamentals.run", None)
    runpy.run_module("cs_fundamentals.run", run_name="__main__")

    # Assertions.
    assert "args" in called and "kwargs" in called
    args = called["args"]
    kwargs = called["kwargs"]
    assert args[0] == "cs_fundamentals.main:app"
    assert kwargs["host"] == "0.0.0.0"
    assert isinstance(kwargs["port"], int)
    assert kwargs["reload"] is True
    assert kwargs["access_log"] is False
    assert isinstance(kwargs.get("log_config"), dict)
    assert isinstance(kwargs.get("log_level"), str)
