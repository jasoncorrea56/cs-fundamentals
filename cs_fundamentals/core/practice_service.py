from __future__ import annotations

from time import perf_counter
from collections.abc import Iterable  # noqa: TC003
from typing import Any

from cs_fundamentals.core.inject import _compile_functions, inject_into_practice
from cs_fundamentals.core.logging_config import get_logger
from cs_fundamentals.core.run_tests import run_pytest

log = get_logger(__name__)


def run_submission(
    *,
    module: str,
    class_name: str | list[str],
    methods: dict[str, str],
    test_files: Iterable[str] | None,
    test_expr: str | None,
) -> dict[str, Any]:
    """
    Compile once -> inject into one or many classes -> run pytest.
    The caller decides which tests to run (or default to automation/ via run_pytest).
    """
    class_names = [class_name] if isinstance(class_name, str) else list(class_name)

    log.info(
        "practice.run_submission.begin",
        extra={
            "target_module": module,
            "class_names": class_names,
            "num_methods": len(methods),
            "test_expr": test_expr,
            "test_files": list(test_files) if test_files is not None else None,
        },
    )

    t0 = perf_counter()
    funcs = _compile_functions(methods)
    t1 = perf_counter()
    log.debug(
        "practice.compile.done",
        extra={"compile_seconds": round(t1 - t0, 6), "compiled": list(funcs.keys())},
    )

    for cls in class_names:
        inject_start = perf_counter()
        inject_into_practice(module, cls, funcs)
        inject_end = perf_counter()
        log.debug(
            "practice.inject.done",
            extra={
                "target_module": module,
                "class_name": cls,
                "inject_seconds": round(inject_end - inject_start, 6),
                "method_count": len(funcs),
            },
        )

    test_start = perf_counter()
    result = run_pytest(
        list(test_files) if test_files is not None else None,
        test_expr,
    )
    test_end = perf_counter()

    log.info(
        "practice.run_submission.end",
        extra={
            "target_module": module,
            "class_names": class_names,
            "pytest_seconds": round(test_end - test_start, 6),
            "summary": result.get("summary"),
            "success": result.get("success"),
            "exit_code": result.get("exit_code"),
        },
    )

    return result
