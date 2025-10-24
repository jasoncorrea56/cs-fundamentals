from __future__ import annotations

import types
import sys
from collections.abc import Callable  # noqa: TC003
from types import SimpleNamespace, ModuleType

import pytest

from cs_fundamentals.core import handler_factory as hf
from cs_fundamentals.core.inject import DisallowedImportError
from cs_fundamentals.models.schemas import MethodsOnly
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


# Force anyio to use asyncio so the plugin doesn't try trio.
@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


# -------------------------- test helpers / fixtures --------------------------


@pytest.fixture(autouse=True)
def restore_hf_namespace(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Ensure we don't leak monkeypatches between tests.
    """
    # Nothing to do up-front; this fixture just gives us an autouse scope.
    # Pytest's monkeypatch fixture will undo per-test patches automatically.
    pass


def _make_dummy_module(name: str = "dummy_mod") -> ModuleType:
    """
    Create a throwaway module with nested classes we can resolve/inject into.
    """
    mod: ModuleType = types.ModuleType(name)

    class Outer:
        class Inner:
            # Provide a placeholder method that we can validate and then replace
            def bar(self) -> str:  # pragma: no cover - behavior validated via replacement
                return "old"

        # Also provide a top-level method for simple (non-dotted) validation use if needed
        def foo(self) -> str:  # pragma: no cover
            return "outer"

    # Attach to module
    setattr(mod, "Outer", Outer)

    # Register in sys.modules for importlib to find it
    sys.modules[name] = mod
    return mod


# ------------------------------- unit tests ----------------------------------


def test_resolve_class_non_dotted_and_dotted() -> None:
    mod = _make_dummy_module("dummy_mod_a")
    # Non-dotted: resolve Outer
    cls_outer = hf._resolve_class("dummy_mod_a", "Outer")
    assert cls_outer is getattr(mod, "Outer")

    # Dotted: resolve Outer.Inner
    cls_inner = hf._resolve_class("dummy_mod_a", "Outer.Inner")
    assert cls_inner is getattr(getattr(mod, "Outer"), "Inner")


def test_validate_methods_exist_flexible_simple_calls_base(monkeypatch: pytest.MonkeyPatch) -> None:
    called: dict[str, Any] = {}

    def fake_base_validate(module_path: str, class_name: str, methods: list[str]) -> None:
        called["args"] = (module_path, class_name, list(methods))

    monkeypatch.setattr(hf, "_base_validate_methods_exist", fake_base_validate)
    hf._validate_methods_exist_flexible("m.pkg", "Classy", ["a", "b"])
    assert called["args"] == ("m.pkg", "Classy", ["a", "b"])


def test_validate_methods_exist_flexible_dotted_success_and_failure() -> None:
    _make_dummy_module("dummy_mod_b")

    # Success: Inner has 'bar'
    hf._validate_methods_exist_flexible("dummy_mod_b", "Outer.Inner", ["bar"])

    # Failure: ask for missing method
    with pytest.raises(AttributeError) as e:
        hf._validate_methods_exist_flexible("dummy_mod_b", "Outer.Inner", ["nope"])
    assert "Unknown method(s) for dummy_mod_b.Outer.Inner: nope" in str(e.value)


def test_inject_extra_non_dotted_calls_compile_and_inject(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_compile(methods: dict[str, str]) -> dict[str, Callable[..., Any]]:
        captured["compiled_from"] = dict(methods)

        def f1(*_a: Any, **_k: Any) -> None:  # pragma: no cover
            return None

        return {"f1": f1}

    def fake_inject(module: str, class_name: str, funcs: dict[str, Callable[..., Any]]) -> None:
        captured["inject_args"] = (module, class_name, set(funcs.keys()))

    # For non-dotted class_name, the flexible validator delegates to base validator.
    # Let it be a no-op here.
    monkeypatch.setattr(hf, "_base_validate_methods_exist", lambda *_a, **_k: None)
    monkeypatch.setattr(hf, "_compile_functions", fake_compile)
    monkeypatch.setattr(hf, "inject_into_practice", fake_inject)

    hf._inject_extra("pkg.m", "SomeClass", {"x": "def x(): pass"})

    assert captured["compiled_from"] == {"x": "def x(): pass"}
    assert captured["inject_args"] == ("pkg.m", "SomeClass", {"f1"})


def test_inject_extra_dotted_replaces_method_in_inner_class(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mod = _make_dummy_module("dummy_mod_c")

    # Ensure validation passes by checking for method name 'bar' (already exists on Inner)
    # We still want to replace it with a new implementation.
    def fake_compile(methods: dict[str, str]) -> dict[str, Callable[..., Any]]:
        def bar(self: Any) -> str:
            return "new"

        return {"bar": bar}

    # Allow flexible validator to run its dotted-path check (hasattr on 'bar' will pass)
    # No monkeypatch needed for validator.

    monkeypatch.setattr(hf, "_compile_functions", fake_compile)

    # Before injection: calling Outer.Inner().bar() -> "old"
    Inner = getattr(getattr(mod, "Outer"), "Inner")
    assert Inner().bar() == "old"

    # Perform injection
    hf._inject_extra("dummy_mod_c", "Outer.Inner", {"bar": "def bar(self): return 'new'"})

    # After injection: behavior should be replaced
    assert Inner().bar() == "new"


# -------------------------- make_submit_handler_from_matrix -------------------


@pytest.mark.anyio
async def test_submit_handler_no_methods_early_error(monkeypatch: pytest.MonkeyPatch) -> None:
    # Minimal target
    target = SimpleNamespace(
        key="k1", module="m1", class_name="C1", test_expr=None, test_files=None, kind="practice"
    )
    monkeypatch.setattr(hf, "get_target", lambda key: target)

    # Make error/success stubs
    monkeypatch.setattr(hf, "error_response", lambda **kw: {"status_code": kw["status_code"], **kw})
    monkeypatch.setattr(hf, "success_response", lambda **kw: {"status_code": 200, **kw})

    handler = hf.make_submit_handler_from_matrix(key="k1")

    # No methods -> early 400
    result = await handler(MethodsOnly(methods=None))
    assert isinstance(result, dict)
    assert result["status_code"] == 400
    assert result["message"] == "No methods provided in payload."


@pytest.mark.anyio
async def test_submit_handler_success_happy_path(monkeypatch: pytest.MonkeyPatch) -> None:
    target = SimpleNamespace(
        key="k2",
        module="m2",
        class_name="C2",
        test_expr="expr",
        test_files=["t.py"],
        kind="practice",
    )
    monkeypatch.setattr(hf, "get_target", lambda key: target)
    monkeypatch.setattr(hf, "_validate_methods_exist_flexible", lambda *a, **k: None)
    # Return a "successful" run result
    run_result = {"success": True, "exit_code": 0, "summary": {"passed": 3}}
    monkeypatch.setattr(hf, "run_submission", lambda **kw: run_result)
    monkeypatch.setattr(hf, "is_pytest_ok", lambda r: True)
    monkeypatch.setattr(
        hf,
        "success_response",
        lambda data, message, payload: {
            "ok": True,
            "data": data,
            "message": message,
            "payload": payload,
        },
    )
    monkeypatch.setattr(hf, "error_response", lambda **kw: {"status_code": kw["status_code"], **kw})

    handler = hf.make_submit_handler_from_matrix(key="k2", success_message="yay")
    result = await handler(MethodsOnly(methods={"f": "def f(): pass"}))
    assert result["ok"] is True
    assert result["data"] == run_result
    assert result["message"] == "yay"
    assert result["payload"]["class_name"] == "C2"


@pytest.mark.anyio
async def test_submit_handler_failure_pytest_not_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    target = SimpleNamespace(
        key="k3", module="m3", class_name="C3", test_expr=None, test_files=None, kind="practice"
    )
    monkeypatch.setattr(hf, "get_target", lambda key: target)
    monkeypatch.setattr(hf, "_validate_methods_exist_flexible", lambda *a, **k: None)
    run_result = {"success": False, "exit_code": 1, "summary": {"failed": 1}}
    monkeypatch.setattr(hf, "run_submission", lambda **kw: run_result)
    monkeypatch.setattr(hf, "is_pytest_ok", lambda r: False)
    monkeypatch.setattr(hf, "format_pytest_summary_tail", lambda s: " (tail)")
    monkeypatch.setattr(
        hf,
        "error_response",
        lambda **kw: {"status_code": kw["status_code"], "message": kw["message"]},
    )

    handler = hf.make_submit_handler_from_matrix(key="k3")
    result = await handler(MethodsOnly(methods={"g": "def g(): pass"}))
    assert result["status_code"] == 400
    assert "Test run failed" in result["message"]
    assert "(tail)" in result["message"]


@pytest.mark.anyio
async def test_submit_handler_with_method_splitter_and_extra_injections(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = SimpleNamespace(
        key="k4", module="m4", class_name="C4", test_expr=None, test_files=None, kind="practice"
    )
    monkeypatch.setattr(hf, "get_target", lambda key: target)
    monkeypatch.setattr(hf, "_validate_methods_exist_flexible", lambda *a, **k: None)
    monkeypatch.setattr(
        hf, "run_submission", lambda **kw: {"success": True, "exit_code": 0, "summary": {}}
    )
    monkeypatch.setattr(hf, "is_pytest_ok", lambda r: True)
    monkeypatch.setattr(hf, "success_response", lambda **kw: {"ok": True})
    calls: list[tuple[str, str, dict[str, str]]] = []

    def fake_inject_extra(m: str, c: str, md: dict[str, str]) -> None:
        calls.append((m, c, md))

    monkeypatch.setattr(hf, "_inject_extra", fake_inject_extra)

    # Splitter returns (primary, extras)
    def splitter(
        methods: dict[str, str],
    ) -> tuple[dict[str, str], list[tuple[str, str, dict[str, str]]]]:
        primary = {"a": methods["a"]}
        extras = [("mX", "Outer.Inner", {"b": "def b(): pass"})]
        return primary, extras

    handler = hf.make_submit_handler_from_matrix(key="k4", method_splitter=splitter)
    res = await handler(MethodsOnly(methods={"a": "def a(): pass", "b": "def b(): pass"}))
    assert res["ok"] is True
    assert calls == [("mX", "Outer.Inner", {"b": "def b(): pass"})]


@pytest.mark.anyio
async def test_submit_handler_disallowed_import_error(monkeypatch: pytest.MonkeyPatch) -> None:
    target = SimpleNamespace(
        key="k5", module="m5", class_name="C5", test_expr=None, test_files=None, kind="practice"
    )
    monkeypatch.setattr(hf, "get_target", lambda key: target)
    monkeypatch.setattr(hf, "_validate_methods_exist_flexible", lambda *a, **k: None)

    def boom(**_kw: Any) -> dict[str, Any]:
        raise DisallowedImportError("nope")

    monkeypatch.setattr(hf, "run_submission", boom)
    monkeypatch.setattr(
        hf,
        "error_response",
        lambda **kw: {"status_code": kw["status_code"], "message": kw["message"]},
    )

    handler = hf.make_submit_handler_from_matrix(key="k5")
    res = await handler(MethodsOnly(methods={"x": "def x(): pass"}))
    assert res["status_code"] == 400
    assert res["message"] == "nope"


@pytest.mark.anyio
async def test_submit_handler_attribute_error(monkeypatch: pytest.MonkeyPatch) -> None:
    target = SimpleNamespace(
        key="k6", module="m6", class_name="C6", test_expr=None, test_files=None, kind="practice"
    )
    monkeypatch.setattr(hf, "get_target", lambda key: target)

    def bad(*_a: Any, **_k: Any) -> None:
        raise AttributeError("method missing")

    monkeypatch.setattr(hf, "_validate_methods_exist_flexible", bad)
    monkeypatch.setattr(
        hf,
        "error_response",
        lambda **kw: {"status_code": kw["status_code"], "message": kw["message"]},
    )

    handler = hf.make_submit_handler_from_matrix(key="k6")
    res = await handler(MethodsOnly(methods={"x": "def x(): pass"}))
    assert res["status_code"] == 400
    assert res["message"] == "method missing"


@pytest.mark.anyio
async def test_submit_handler_generic_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    target = SimpleNamespace(
        key="k7", module="m7", class_name="C7", test_expr=None, test_files=None, kind="practice"
    )
    monkeypatch.setattr(hf, "get_target", lambda key: target)
    monkeypatch.setattr(hf, "_validate_methods_exist_flexible", lambda *a, **k: None)

    def kaboom(**_kw: Any) -> dict[str, Any]:
        raise RuntimeError("boom")

    monkeypatch.setattr(hf, "run_submission", kaboom)
    monkeypatch.setattr(
        hf,
        "error_response",
        lambda **kw: {"status_code": kw["status_code"], "message": kw["message"]},
    )

    handler = hf.make_submit_handler_from_matrix(key="k7")
    res = await handler(MethodsOnly(methods={"x": "def x(): pass"}))
    assert res["status_code"] == 400
    assert "boom" in res["message"]
    # Should contain traceback text too
    assert "Traceback" in res["message"]
