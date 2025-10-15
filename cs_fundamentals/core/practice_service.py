from __future__ import annotations

from collections.abc import Iterable  # noqa: TC003
from typing import Any

from cs_fundamentals.core.inject import _compile_functions, inject_into_practice
from cs_fundamentals.core.run_tests import run_pytest


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

    funcs = _compile_functions(methods)

    for cls in class_names:
        inject_into_practice(module, cls, funcs)

    return run_pytest(
        list(test_files) if test_files is not None else None,
        test_expr,
    )
