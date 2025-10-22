from __future__ import annotations

from typing import Any, TYPE_CHECKING
from collections.abc import Callable  # noqa: TC003

from cs_fundamentals.core import practice_service as ps

if TYPE_CHECKING:
    import pytest


def _result(success: bool = True) -> dict[str, Any]:
    return {"success": success, "exit_code": 0 if success else 1, "summary": {"passed": 1}}


# ------------------------------ single class ------------------------------


def test_run_submission_single_class_happy_path(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: dict[str, Any] = {}

    # Stub compiled functions (pretend we compiled one function)
    compiled_funcs: dict[str, Callable[..., Any]] = {"f": lambda *_a, **_k: None}

    def fake_compile(methods: dict[str, str]) -> dict[str, Callable[..., Any]]:
        calls["compiled_methods"] = dict(methods)
        return compiled_funcs

    def fake_inject(module: str, class_name: str, funcs: dict[str, Callable[..., Any]]) -> None:
        calls.setdefault("injects", []).append((module, class_name, set(funcs.keys())))

    def fake_run_pytest(files: list[str] | None, expr: str | None) -> dict[str, Any]:
        calls["pytest_args"] = (files, expr)
        return _result(True)

    monkeypatch.setattr(ps, "_compile_functions", fake_compile)
    monkeypatch.setattr(ps, "inject_into_practice", fake_inject)
    monkeypatch.setattr(ps, "run_pytest", fake_run_pytest)

    result: dict[str, Any] = ps.run_submission(
        module="pkg.mod",
        class_name="PracticeThing",
        methods={"f": "def f(): pass"},
        test_files=["tests/test_a.py", "tests/test_b.py"],
        test_expr="PracticeThing and f",
    )

    assert result == _result(True)
    assert calls["compiled_methods"] == {"f": "def f(): pass"}
    # Injected once for the single class
    assert calls["injects"] == [("pkg.mod", "PracticeThing", {"f"})]
    # run_pytest receives a list for files and the expr
    assert calls["pytest_args"] == (["tests/test_a.py", "tests/test_b.py"], "PracticeThing and f")


# ----------------------------- multiple classes -----------------------------


def test_run_submission_multiple_classes_inject_each(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: dict[str, Any] = {}

    compiled_funcs: dict[str, Callable[..., Any]] = {"g": lambda *_a, **_k: None}

    monkeypatch.setattr(ps, "_compile_functions", lambda methods: compiled_funcs)

    def fake_inject(module: str, class_name: str, funcs: dict[str, Callable[..., Any]]) -> None:
        calls.setdefault("injects", []).append((module, class_name, set(funcs.keys())))

    monkeypatch.setattr(ps, "inject_into_practice", fake_inject)
    monkeypatch.setattr(ps, "run_pytest", lambda files, expr: _result(True))

    result: dict[str, Any] = ps.run_submission(
        module="pkg.other",
        class_name=["C1", "C2", "C3"],
        methods={"g": "def g(): pass"},
        test_files=("tests/a.py", "tests/b.py"),  # Any Iterable allowed
        test_expr=None,
    )

    assert result == _result(True)
    # Injected once per class in the provided list
    assert calls["injects"] == [
        ("pkg.other", "C1", {"g"}),
        ("pkg.other", "C2", {"g"}),
        ("pkg.other", "C3", {"g"}),
    ]


# ----------------------------- test_files = None -----------------------------


def test_run_submission_none_test_files(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: dict[str, Any] = {}

    monkeypatch.setattr(ps, "_compile_functions", lambda methods: {"h": lambda: None})
    monkeypatch.setattr(ps, "inject_into_practice", lambda *_a, **_k: None)

    def fake_run_pytest(files: list[str] | None, expr: str | None) -> dict[str, Any]:
        seen["files"] = files
        seen["expr"] = expr
        return _result(False)

    monkeypatch.setattr(ps, "run_pytest", fake_run_pytest)

    result: dict[str, Any] = ps.run_submission(
        module="pkg.none",
        class_name="C",
        methods={"h": "def h(): pass"},
        test_files=None,  # Ensure None flows through
        test_expr=None,
    )

    assert result == _result(False)
    assert seen["files"] is None
    assert seen["expr"] is None
