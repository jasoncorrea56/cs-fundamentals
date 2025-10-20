from __future__ import annotations

import importlib
from collections.abc import Iterable  # noqa: TC003


def validate_methods_exist(module_path: str, class_name: str, methods: Iterable[str]) -> None:
    """
    Ensure every provided method name exists on the target class.
    Raises AttributeError with a helpful message if not.
    """
    mod = importlib.import_module(module_path)
    cls = getattr(mod, class_name)
    missing = [m for m in methods if not hasattr(cls, m)]
    if missing:
        raise AttributeError(
            f"Unknown method(s) for {module_path}.{class_name}: {', '.join(missing)}"
        )
