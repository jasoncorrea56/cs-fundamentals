from __future__ import annotations

import sys
import runpy
import pytest
import warnings
from typing import TYPE_CHECKING

import cs_fundamentals.admin as admin

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch
    from _pytest.logging import LogCaptureFixture


warnings.filterwarnings("ignore", category=RuntimeWarning)


def test_main_no_args_exits(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """Should exit(1) and log usage when no arguments are passed."""
    monkeypatch.setattr(sys, "argv", ["admin.py"])
    with pytest.raises(SystemExit) as e:
        admin.main()
    assert e.value.code == 1
    assert any("Usage:" in m for m in caplog.text.splitlines())


def test_main_health_logs_ok(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """Should log a health message and not exit for known task 'health'."""
    monkeypatch.setattr(sys, "argv", ["admin.py", "health"])
    admin.main()
    assert any("healthy" in m.lower() for m in caplog.text.splitlines())


def test_main_unknown_task_exits(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """Should exit(1) and log error for unknown task."""
    monkeypatch.setattr(sys, "argv", ["admin.py", "unknown_task"])
    with pytest.raises(SystemExit) as e:
        admin.main()
    assert e.value.code == 1
    assert any("Unknown admin task" in m for m in caplog.text.splitlines())


def test_main_entrypoint_block(monkeypatch: MonkeyPatch, caplog: LogCaptureFixture) -> None:
    """Covers the __main__ block without duplicate import warning."""
    monkeypatch.setattr(sys, "argv", ["cs_fundamentals/admin.py", "health"])
    sys.modules.pop("cs_fundamentals.admin", None)  # remove cached import
    result = runpy.run_module("cs_fundamentals.admin", run_name="__main__")
    assert result.get("__name__") == "__main__"
    assert any("healthy" in line.lower() for line in caplog.text.splitlines())
