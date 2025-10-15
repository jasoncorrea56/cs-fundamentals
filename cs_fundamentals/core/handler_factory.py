from __future__ import annotations

import importlib
import traceback
from collections.abc import Callable, Iterable  # noqa: TC003
from typing import Any

from cs_fundamentals.core.inject import (
    DisallowedImportError,
    _compile_functions,
    inject_into_practice,
)
from cs_fundamentals.core.practice_service import run_submission
from cs_fundamentals.core.response import error_response, success_response
from cs_fundamentals.core.test_matrix import TestTarget, get_target
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001
from cs_fundamentals.core.validation import (
    validate_methods_exist as _base_validate_methods_exist,
)

# method_splitter: (methods) -> (primary_methods, extra_injections)
# extra_injections: list of tuples (module, class_name, methods_dict)
MethodSplitter = Callable[
    [dict[str, str]], tuple[dict[str, str], list[tuple[str, str, dict[str, str]]]]
]


def _resolve_class(module_path: str, dotted_class: str) -> type:
    """
    Resolve 'pkg.mod' + 'Outer.Inner.More' -> final class/type object.
    """
    mod = importlib.import_module(module_path)
    obj: Any = mod
    for part in dotted_class.split("."):
        obj = getattr(obj, part)
    return obj


def _validate_methods_exist_flexible(
    module_path: str, class_name: str, methods: Iterable[str]
) -> None:
    """
    Wrapper that uses the original validate for simple classes and
    supports dotted/nested classes by resolving then checking hasattr().
    """
    if "." not in class_name:
        # Use the original helper for simple (non-nested) classes.
        _base_validate_methods_exist(module_path, class_name, methods)
        return

    # Nested class path: resolve step-by-step, then check attributes.
    cls = _resolve_class(module_path, class_name)
    missing = [m for m in methods if not hasattr(cls, m)]
    if missing:
        raise AttributeError(
            f"Unknown method(s) for {module_path}.{class_name}: {', '.join(missing)}"
        )


def _inject_extra(module: str, class_name: str, methods: dict[str, str]) -> None:
    """
    Inject methods into a class. Supports nested classes via 'Outer.Inner' in class_name.
    """
    # Validate methods against the target (including nested) before compiling/injecting.
    _validate_methods_exist_flexible(module, class_name, methods.keys())

    if "." not in class_name:
        funcs = _compile_functions(methods)
        inject_into_practice(module, class_name, funcs)
        return

    # Nested class injection: resolve and setattr
    outer_name, inner_name = class_name.split(".", 1)
    mod = importlib.import_module(module)
    outer_cls = getattr(mod, outer_name)
    inner_cls = getattr(outer_cls, inner_name)

    funcs = _compile_functions(methods)
    for name, fn in funcs.items():
        # Leave instance methods as normal callables; don't wrap staticmethod/classmethod here.
        setattr(inner_cls, name, fn)


def make_submit_handler_from_matrix(
    *,
    key: str,
    success_message: str | None = None,
    method_splitter: MethodSplitter | None = None,
) -> Callable[[MethodsOnly], Any]:
    """
    Build a /submit handler from a matrix key.
    Optional method_splitter to support multi-/nested-class injections before running tests.
    """
    target: TestTarget = get_target(key)
    message: str = (
        success_message or f"All tests for '{target.key}' executed successfully."
    )

    async def _handler(payload: MethodsOnly) -> dict[str, Any]:
        try:
            if not payload.methods:
                return error_response(
                    status_code=400,
                    message="No methods provided in payload.",
                    payload={"key": key, "methods": payload.methods},
                )

            primary_methods = payload.methods
            extra_injections: list[tuple[str, str, dict[str, str]]] = []

            if method_splitter is not None:
                primary_methods, extra_injections = method_splitter(payload.methods)

            # 1) Validate the primary target methods exist on the class (supports nested list via practice_service,
            #    but here target.class_name is typically a single class for patterns/DS endpoints).
            _validate_methods_exist_flexible(
                target.module,
                target.class_name
                if isinstance(target.class_name, str)
                else target.class_name[0],
                primary_methods.keys(),
            )

            # 2) Pre-inject any extra targets (e.g., nested PracticeGraphProblems.UnionFind)
            #    with validation per extra target.
            for mod, cls, methods in extra_injections:
                _inject_extra(mod, cls, methods)

            # 3) Run the main target
            result = run_submission(
                module=target.module,
                class_name=target.class_name,
                methods=primary_methods,
                test_files=target.test_files,
                test_expr=target.test_expr,
            )

            meta = {
                "key": target.key,
                "module": target.module,
                "class_name": target.class_name,
                "test_files": target.test_files,
                "test_expr": target.test_expr,
                "kind": target.kind,
            }

            # Reflect pytest outcome in HTTP body
            if not result.get("success", False):
                # Build a helpful message from the parsed summary if available
                summary = result.get("summary") or {}
                parts = []
                for k in ("failed", "errors", "skipped", "collected", "deselected"):
                    if k in summary:
                        parts.append(f"{k}={summary[k]}")
                tail = f" ({', '.join(parts)})" if parts else ""
                return error_response(
                    status_code=400,
                    message=f"Test run failed{tail}. See stdout/stderr for details.",
                    payload={"result": result, **meta, "methods": payload.methods},
                )

            return success_response(data=result, message=message, payload=meta)

        except DisallowedImportError as diexc:
            return error_response(
                status_code=400,
                message=str(diexc),
                payload={"key": key, "methods": payload.methods},
            )

        except AttributeError as aexc:
            # Clean “unknown method(s)” or “unknown class” feedback from validation.
            return error_response(
                status_code=400,
                message=str(aexc),
                payload={"key": key, "methods": payload.methods},
            )

        except Exception as exc:  # noqa: BLE001
            tb = traceback.format_exc()
            return error_response(
                status_code=400,
                message=f"{str(exc)}\n\n{str(tb)}",
                payload={"key": key, "methods": payload.methods},
            )

    return _handler
