import ast
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

# Deny-list of callable names inside submitted code
_DENIED_CALLS = {
    "eval",
    "exec",
    "open",
    "__import__",
    "compile",
    "input",
    "globals",
    "locals",
    "vars",
    "dir",
    "getattr",
    "setattr",
    "delattr",
}


class DisallowedImportError(ImportError):
    """Custom import error for sandboxed submission code."""


class _SafeSubmissionValidator(ast.NodeVisitor):
    """
    Rejects modules that contain anything other than def statements at top level,
    and forbids calls to dangerous builtins and dunder access inside functions.
    """

    def visit_Module(self, node: ast.Module) -> None:
        # Allow: module docstring, function defs, and SAFE simple assignments.
        for n in node.body:
            if (
                isinstance(n, ast.Expr)
                and isinstance(n.value, ast.Constant)
                and isinstance(n.value.value, str)
            ):
                continue  # Module docstring

            if isinstance(n, ast.FunctionDef):
                continue

            # Allow simple top-level assignments of literal data OR safe builtin refs
            if isinstance(n, ast.Assign):
                # Targets must be plain names; value must be a safe literal expr
                if all(isinstance(t, ast.Name) for t in n.targets) and _is_safe_toplevel_value(
                    n.value
                ):
                    continue
                raise SyntaxError(
                    "Only function definitions or simple literal/builtin assignments allowed at top level."
                )

            if isinstance(n, ast.AnnAssign):
                # Single name target, simple literal value (i.e. x: int = 3)
                if isinstance(n.target, ast.Name) and (
                    n.value is None or _is_safe_toplevel_value(n.value)
                ):
                    continue
                raise SyntaxError(
                    "Only function definitions or simple literal/builtin assignments allowed at top level."
                )

            raise SyntaxError(f"Only function definitions are allowed (found {type(n).__name__}).")

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        # Allow exactly:
        #   1) object.__new__   (for classic singleton)
        #   2) <name>.__dict__ = ... (STORE context only; for Borg state sharing)
        if isinstance(node.attr, str) and node.attr.startswith("__") and node.attr.endswith("__"):
            base_is_object_new = (
                node.attr == "__new__"
                and isinstance(node.value, ast.Name)
                and node.value.id == "object"
            )
            dict_store = node.attr == "__dict__" and isinstance(node.ctx, ast.Store)
            if not (base_is_object_new or dict_store):
                raise SyntaxError("Dunder attribute access is not allowed.")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        # Block denied call names: eval(...), exec(...), open(...), etc.
        if isinstance(node.func, ast.Name) and node.func.id in _DENIED_CALLS:
            raise SyntaxError(f"Call to '{node.func.id}' is not allowed.")
        self.generic_visit(node)


def _is_safe_literal_expr(node: ast.AST | None) -> bool:
    """
    Allow only literals and literal containers.
    Note: Dict keys can be None in the AST for '**' unpack; treat as unsafe.
    """
    if node is None:
        return False
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        return all(_is_safe_literal_expr(elt) for elt in node.elts)
    if isinstance(node, ast.Dict):
        return all(
            _is_safe_literal_expr(k) and _is_safe_literal_expr(v)
            for k, v in zip(node.keys, node.values)
        )
    if (
        isinstance(node, ast.UnaryOp)
        and isinstance(node.op, (ast.UAdd, ast.USub))
        and isinstance(node.operand, ast.Constant)
    ):
        return isinstance(node.operand.value, (int, float, complex))
    return False


def _is_safe_toplevel_value(node: ast.AST) -> bool:
    """
    Top-level assignment can also reference a safe builtin by name (i.e. x = print)
    """
    if _is_safe_literal_expr(node):
        return True
    return bool(isinstance(node, ast.Name) and node.id in SAFE_BUILTINS)


def _validate_source_is_safe(src: str) -> ast.Module:
    """
    Validate source safety before injection
    """
    tree = ast.parse(src, filename="<submission>", mode="exec")
    _SafeSubmissionValidator().visit(tree)
    return tree


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

        # Validate AST and execute in sandbox with restricted builtins/imports.
        try:
            tree = _validate_source_is_safe(src)
            code = compile(tree, "<submission>", "exec")

            exec(
                code, safe_globals, local_ns
            )  # nosemgrep: python.lang.security.audit.exec-detected.exec-detected

        except SyntaxError as syn:
            raise SyntaxError(
                f"SyntaxError compiling method '{name}': {syn.msg} (line {syn.lineno})"
            ) from syn

        except Exception as exc:
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
        f.__globals__.setdefault(n, f)  # Bind the function's name to itself if missing

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
