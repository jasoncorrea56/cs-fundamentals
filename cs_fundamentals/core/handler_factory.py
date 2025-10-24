from __future__ import annotations

import importlib
import traceback
from collections.abc import Awaitable, Callable, Iterable  # noqa: TC003
from typing import TYPE_CHECKING

from fastapi.responses import JSONResponse

from cs_fundamentals.core.inject import (
    DisallowedImportError,
    _compile_functions,
    inject_into_practice,
)
from cs_fundamentals.core.logging_config import get_logger
from cs_fundamentals.core.practice_service import run_submission
from cs_fundamentals.core.response import (
    error_response,
    success_response,
    format_pytest_summary_tail,
    is_pytest_ok,
)
from cs_fundamentals.core.test_matrix import TestTarget, get_target
from cs_fundamentals.core.validation import (
    validate_methods_exist as _base_validate_methods_exist,
)
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001

if TYPE_CHECKING:
    from typing import Any


# method_splitter: (methods) -> (primary_methods, extra_injections)
# extra_injections: list of tuples (module, class_name, methods_dict)
MethodSplitter = Callable[
    [dict[str, str]], tuple[dict[str, str], list[tuple[str, str, dict[str, str]]]]
]

log = get_logger(__name__)


def _resolve_class(module_path: str, dotted_class: str) -> type[Any]:
    """
    Resolve 'pkg.mod' + 'Outer.Inner.More' -> final class/type object.
    Raises TypeError if the final attribute is not a class.
    """
    mod = importlib.import_module(module_path)
    obj: Any = mod
    for part in dotted_class.split("."):
        obj = getattr(obj, part)
    if not isinstance(obj, type):
        raise TypeError(f"Resolved attribute is not a class: {module_path}.{dotted_class}")
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
) -> Callable[[MethodsOnly], Awaitable[JSONResponse]]:
    """
    Build a /submit handler from a matrix key.
    Optional method_splitter to support multi-/nested-class injections before running tests.
    """
    target: TestTarget = get_target(key)
    message: str = success_message or f"All tests for '{target.key}' executed successfully."

    log.debug(
        "handler_factory.make_submit_handler_from_matrix.init",
        extra={
            "target_key": target.key,
            "target_module": target.module,
            "class_name": target.class_name,
            "test_expr": target.test_expr,
            "test_files": target.test_files,
            "kind": target.kind,
            "has_splitter": method_splitter is not None,
        },
    )

    async def _handler(payload: MethodsOnly) -> JSONResponse:
        log.info(
            "submit.start",
            extra={
                "target_key": target.key,
                "target_module": target.module,
                "class_name": target.class_name,
                "num_methods": len(payload.methods or {}),
            },
        )
        try:
            if not payload.methods:
                log.warning("submit.no_methods", extra={"target_key": target.key})
                return error_response(
                    status_code=400,
                    message="No methods provided in payload.",
                    payload={"key": key, "methods": payload.methods},
                )

            primary_methods = payload.methods
            extra_injections: list[tuple[str, str, dict[str, str]]] = []

            if method_splitter is not None:
                primary_methods, extra_injections = method_splitter(payload.methods)
                log.debug(
                    "submit.methods.split",
                    extra={
                        "target_key": target.key,
                        "primary_count": len(primary_methods),
                        "extra_count": len(extra_injections),
                        "extra_targets": [
                            {
                                "target_module": m,
                                "class_name": c,
                                "method_count": len(md),
                            }
                            for (m, c, md) in extra_injections
                        ],
                    },
                )

            # 1) Validate primary target methods
            _validate_methods_exist_flexible(
                target.module,
                target.class_name if isinstance(target.class_name, str) else target.class_name[0],
                primary_methods.keys(),
            )
            log.debug(
                "submit.methods.validated",
                extra={
                    "target_key": target.key,
                    "validated_methods": list(primary_methods.keys()),
                },
            )

            # 2) Pre-inject extras
            for mod, cls, methods in extra_injections:
                log.debug(
                    "submit.inject_extra.begin",
                    extra={
                        "target_key": target.key,
                        "target_module": mod,
                        "class_name": cls,
                        "method_count": len(methods),
                        "methods": list(methods.keys()),
                    },
                )
                _inject_extra(mod, cls, methods)
                log.debug(
                    "submit.inject_extra.done",
                    extra={"target_key": target.key, "target_module": mod, "class_name": cls},
                )

            # 3) Run tests
            log.info(
                "submit.run_tests.begin",
                extra={
                    "target_key": target.key,
                    "target_module": target.module,
                    "class_name": target.class_name,
                },
            )
            result = run_submission(
                module=target.module,
                class_name=target.class_name,
                methods=primary_methods,
                test_files=target.test_files,
                test_expr=target.test_expr,
            )
            log.info(
                "submit.run_tests.done",
                extra={
                    "target_key": target.key,
                    "summary": result.get("summary"),
                    "success": result.get("success"),
                    "exit_code": result.get("exit_code"),
                },
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
            if not is_pytest_ok(result):
                tail = format_pytest_summary_tail(result.get("summary"))
                log.warning(
                    "submit.run_tests.failed",
                    extra={
                        "target_key": target.key,
                        "summary": result.get("summary"),
                        "exit_code": result.get("exit_code"),
                    },
                )
                return error_response(
                    status_code=400,
                    message=f"Test run failed{tail}. See stdout/stderr for details.",
                    payload={"result": result, **meta, "methods": payload.methods},
                )

            log.info(
                "submit.success", extra={"target_key": target.key, "summary": result.get("summary")}
            )
            return success_response(data=result, message=message, payload=meta)

        except DisallowedImportError as diexc:
            log.warning(
                "submit.disallowed_import",
                extra={"target_key": target.key, "error": str(diexc)},
            )
            return error_response(
                status_code=400,
                message=str(diexc),
                payload={"key": key, "methods": payload.methods},
            )

        except AttributeError as aexc:
            log.warning(
                "submit.validation_error",
                extra={"target_key": target.key, "error": str(aexc)},
            )
            return error_response(
                status_code=400,
                message=str(aexc),
                payload={"key": key, "methods": payload.methods},
            )

        except Exception as exc:  # noqa: BLE001
            tb = traceback.format_exc()
            log.exception(
                "submit.unhandled_exception",
                extra={"target_key": target.key, "error": str(exc)},
            )
            return error_response(
                status_code=400,
                message=f"{str(exc)}\n\n{str(tb)}",
                payload={"key": key, "methods": payload.methods},
            )

    return _handler
