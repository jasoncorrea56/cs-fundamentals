from collections.abc import Mapping
from importlib import import_module
from types import FunctionType
from typing import Any

# Allow-list for user code imports
SAFE_MODULES: set[str] = {
    "collections",
    "math",
    "itertools",
    "functools",
    "heapq",
    "statistics",
    "sys",
    "threading",
}


class DisallowedImportError(ImportError):
    """Custom import error for sandboxed submission code."""


def _safe_import(
    name: str,
    globals: Any | None = None,
    locals: Any | None = None,
    fromlist: tuple[str, ...] = (),
    level: int = 0,
) -> Any:
    """
    Only imports sanctioned packages. Raises DisallowedImportError for user code clarity.
    """
    root = name.split(".", 1)[0]
    if root not in SAFE_MODULES:
        raise DisallowedImportError(
            f"Import of '{name}' is not allowed in submissions. "
            "Your code may only use built-in or whitelisted modules "
            "(e.g. math, collections, heapq, itertools)."
        )

    return __import__(name, globals, locals, fromlist, level)


SAFE_BUILTINS: dict[str, object] = {
    "__import__": _safe_import,
    # Primitive types and constructors
    "int": int,
    "str": str,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
    # Core functions
    "range": range,
    "len": len,
    "min": min,
    "max": max,
    "sum": sum,
    "enumerate": enumerate,
    "sorted": sorted,
    "abs": abs,
    "map": map,
    "filter": filter,
    "any": any,
    "all": all,
    "hasattr": hasattr,
    "object": object,
    "zip": zip,
    "print": print,  # optional, helps debugging
}


def _compile_functions(src_by_name: Mapping[str, str]) -> dict[str, FunctionType]:
    """
    Compile a mapping of method name -> function source (full 'def ...' declarations).
    Returns a mapping of name -> live function objects.

    Preserves two-phase behavior:
      1) compile each submitted function in a minimal globals dict
      2) wire up recursion / cross-calls by injecting functions into each other's globals
    """
    compiled: dict[str, FunctionType] = {}

    # 1) Compile each function in its own safe globals dict with minimal builtins.
    for name, src in src_by_name.items():
        safe_globals: dict[str, Any] = {"__builtins__": SAFE_BUILTINS.copy()}
        local_ns: dict[str, Any] = {}

        try:
            # Exec the submitted source into the sandboxed globals/local namespace.
            exec(src, safe_globals, local_ns)  # noqa: S102 (exec intentional in sandbox)
        except SyntaxError as syn:  # give a clear, actionable error
            raise SyntaxError(
                f"SyntaxError compiling method '{name}': {syn.msg} (line {syn.lineno})"
            ) from syn
        except Exception as exc:
            # Generic compile-time error (NameError, TypeError while defining defaults, etc.)
            raise RuntimeError(f"Error compiling method '{name}': {exc}") from exc

        fn = local_ns.get(name)
        if not callable(fn):
            raise ValueError(f"Function '{name}' not defined by provided source.")

        # Ensure we have an actual function object
        if not isinstance(fn, FunctionType):
            raise ValueError(f"Object '{name}' defined but is not a function.")

        compiled[name] = fn

    # 2) Enable recursion and cross-calls:
    #    - bind each function name into its own globals so recursion by name works
    #    - bind all compiled functions into each other's globals so cross-calls work
    for n, f in compiled.items():
        # Bind the function's name to itself if missing
        f.__globals__.setdefault(n, f)
    for n, f in compiled.items():
        for other_name, other_fn in compiled.items():
            f.__globals__.setdefault(other_name, other_fn)

    return compiled


def inject_into_practice(
    module_name: str,
    class_name: str,
    funcs: Mapping[str, FunctionType],
    extra_globals: dict[str, Any] | None = None,
) -> None:
    """
    Attach compiled functions to the given Practice* class.

    - Preserves descriptor semantics (staticmethod/classmethod) if the stub had them.
    - Binds common helper symbols from the owning module (e.g., Node) into each function's globals
      so user code like `Node(...)` works without additional imports.
    """
    mod = import_module(module_name)
    cls = getattr(mod, class_name)

    # Collect symbols from the owner module that are safe/useful for practice code.
    # Add more here as you add DS/pattern modules that expose helpers.
    discovered: dict[str, Any] = {}
    for sym in ("Node", "BinaryTreeNode", "TreeNode", "ListNode"):
        if hasattr(mod, sym):
            discovered[sym] = getattr(mod, sym)

    if extra_globals:
        discovered.update(extra_globals)

    for name, fn in funcs.items():
        # Make sure user functions can see the discovered symbols
        try:
            fn.__globals__.update(discovered)
        except Exception:
            # If something odd slips in (shouldn't), don't let it break injection
            for k, v in discovered.items():
                fn.__globals__.setdefault(k, v)

        # Preserve descriptor style from the existing stub, if any
        if hasattr(cls, name):
            raw = cls.__dict__.get(name, getattr(cls, name))
            if isinstance(raw, staticmethod):
                setattr(cls, name, staticmethod(fn))
            elif isinstance(raw, classmethod):
                setattr(cls, name, classmethod(fn))
            else:
                setattr(cls, name, fn)
        else:
            # No prior stub; assign as a plain instance method
            setattr(cls, name, fn)
