from __future__ import annotations

import types
import sys
from pathlib import Path
from typing import Any

import pytest

from cs_fundamentals.core import run_tests as rt


# ---------------------------- _find_repo_root() ----------------------------


def test_find_repo_root_returns_first_dir_with_pyproject(tmp_path: Path) -> None:
    d1 = tmp_path / "a" / "b" / "c"
    d1.mkdir(parents=True)
    (tmp_path / "a" / "pyproject.toml").write_text("[build-system]\n")
    result = rt._find_repo_root(d1)
    assert result == tmp_path / "a"


def test_find_repo_root_fallback_to_anchor(tmp_path: Path) -> None:
    root = rt._find_repo_root(tmp_path)
    # It should return either Path(tmp_path.anchor) or tmp_path itself
    assert isinstance(root, Path)
    assert root.exists() or root == Path(tmp_path.anchor)


# --------------------------- _parse_pytest_summary() ---------------------------


def test_parse_pytest_summary_basic_variants() -> None:
    s1 = "10 passed in 0.23s"
    summary1 = rt._parse_pytest_summary(s1)
    assert summary1.passed == 10
    assert summary1.duration_seconds == pytest.approx(0.23)
    assert summary1.collected == 10

    s2 = "9 passed, 1 skipped in 0.45s"
    summary2 = rt._parse_pytest_summary(s2)
    assert summary2.passed == 9
    assert summary2.skipped == 1
    assert summary2.collected == 10

    s3 = "8 passed, 1 failed, 1 xfailed in 1.23s"
    summary3 = rt._parse_pytest_summary(s3)
    assert summary3.failed == 1
    assert summary3.xfailed == 1
    assert summary3.collected == 10


def test_parse_pytest_summary_no_tests_and_errors_key() -> None:
    s4 = "no tests ran in 0.01s"
    summary4 = rt._parse_pytest_summary(s4)
    assert summary4.collected == 0
    assert isinstance(summary4.raw, str)

    s5 = "no tests collected"
    summary5 = rt._parse_pytest_summary(s5)
    assert summary5.collected == 0


def test_parse_pytest_summary_handles_duration_and_partial_counts() -> None:
    s = "5 passed, 1 errors in 1.00s"
    result = rt._parse_pytest_summary(s)
    assert result.errors == 1
    assert result.duration_seconds == 1.0
    assert result.collected == 6


def test_parse_pytest_summary_blank_input() -> None:
    s = ""
    result = rt._parse_pytest_summary(s)
    assert isinstance(result, rt.PytestSummary)
    assert result.duration_seconds is None


# --------------------------- _resolve_targets() ---------------------------


def test_resolve_targets_none_and_absolute(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(rt, "TEST_ROOT", tmp_path / "automation")
    absfile = tmp_path / "some_abs_test.py"
    paths = rt._resolve_targets([str(absfile)])
    assert paths == [str(absfile)]

    none_case = rt._resolve_targets(None)
    assert none_case == [str(rt.TEST_ROOT)]


def test_resolve_targets_relative_paths(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(rt, "TEST_ROOT", tmp_path / "automation")
    paths = rt._resolve_targets(
        ["automation/test_a.py", "relative/test_b.py", "./automation/test_c.py"]
    )
    assert all(str(rt.TEST_ROOT) in p for p in paths)
    # Should not duplicate prefix
    assert "automation/automation" not in " ".join(paths)


# --------------------------- run_pytest() ---------------------------


def test_run_pytest_builds_args_and_calls_pytest(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    called: dict[str, Any] = {}

    # Fake _resolve_targets
    monkeypatch.setattr(rt, "_resolve_targets", lambda tf: ["tests/test_sample.py"])

    # Create dummy pytest.main
    def fake_pytest_main(args: list[str]) -> int:
        called["args"] = args
        return 0

    fake_pytest = types.SimpleNamespace(main=fake_pytest_main)
    monkeypatch.setitem(sys.modules, "pytest", fake_pytest)

    # Make _parse_pytest_summary return a real PytestSummary
    monkeypatch.setattr(rt, "_parse_pytest_summary", lambda stdout: rt.PytestSummary(passed=1))

    result = rt.run_pytest(test_files=["tests/test_sample.py"], test_expr="expr")

    # Assertions unchanged...
    assert "args" in called
    assert any("tests/test_sample.py" in a for a in called["args"])
    assert isinstance(result, dict)
    assert result["success"] is True
    assert "summary" in result
    assert "stdout" in result
    assert "stderr" in result
    assert "exit_code" in result


def test_run_pytest_failure_exit_code(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(rt, "_resolve_targets", lambda tf: ["tests/test_fail.py"])

    # Dummy pytest.main returning nonzero
    def fake_main(args: list[str]) -> int:
        return 2

    fake_pytest = types.SimpleNamespace(main=fake_main)
    import sys

    monkeypatch.setitem(sys.modules, "pytest", fake_pytest)

    # Bypass heavy imports
    monkeypatch.setattr(rt, "_parse_pytest_summary", lambda s: rt.PytestSummary(passed=0, failed=1))
    result = rt.run_pytest(["tests/test_fail.py"])
    assert result["success"] is False
    assert result["exit_code"] == 2
