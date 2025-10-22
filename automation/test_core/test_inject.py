from __future__ import annotations

import sys
import types
from types import ModuleType, FunctionType

import pytest

from cs_fundamentals.core import inject as inj


# ------------------------------ _safe_import ------------------------------


def test_safe_import_allows_whitelisted_and_blocks_others() -> None:
    # Allowed root modules
    for name in (
        "math",
        "collections",
        "heapq",
        "itertools",
        "functools",
        "statistics",
        "sys",
        "threading",
    ):
        mod = inj._safe_import(name)
        assert mod is sys.modules[name]

    # Disallowed modules
    with pytest.raises(inj.DisallowedImportError):
        inj._safe_import("os")
    with pytest.raises(inj.DisallowedImportError):
        inj._safe_import("subprocess")
    with pytest.raises(inj.DisallowedImportError):
        inj._safe_import("pathlib")


# --------------------------- _compile_functions ---------------------------


def test_compile_functions_single_and_multiple_with_recursion_and_crosscalls() -> None:
    sources: dict[str, str] = {
        "fact": """
def fact(n):
    if n <= 1:
        return 1
    return n * fact(n-1)
""",
        "g": """
def g(x):
    return x + 1
""",
        "f": """
def f(x):
    return g(x) * 2
""",
    }
    funcs: dict[str, FunctionType] = inj._compile_functions(sources)

    # Check that recursion works
    assert funcs["fact"](5) == 120

    # Check that cross-calls work
    assert funcs["f"](3) == 8
    assert funcs["g"](10) == 11


def test_compile_functions_syntax_error_and_compile_time_error() -> None:
    # Syntax error (missing colon)
    with pytest.raises(SyntaxError) as e:
        inj._compile_functions({"bad": "def bad(x)\n    return x"})
    assert "SyntaxError compiling method 'bad'" in str(e.value)

    # Compile-time error: default value referencing undefined name -> NameError during def
    with pytest.raises(RuntimeError) as e2:
        inj._compile_functions({"oops": "def oops(x=UNKNOWN):\n    return x"})
    assert "Error compiling method 'oops'" in str(e2.value)


def test_compile_functions_missing_named_function_and_non_function_object() -> None:
    # Provided name doesn't match function defined inside
    with pytest.raises(ValueError) as e1:
        inj._compile_functions({"expected": "def other():\n    return 1"})
    assert "Function 'expected' not defined" in str(e1.value)

    # Name exists but is not callable -> should say "not defined"
    with pytest.raises(ValueError) as e2:
        inj._compile_functions({"x": "x = 3"})
    assert "Function 'x' not defined by provided source." in str(e2.value)
    # Name is callable but not a real function (i.e. a built-in) -> "not a function"
    src_callable_not_function = "x = print"
    with pytest.raises(ValueError) as e3:
        inj._compile_functions({"x": src_callable_not_function})
    assert "Object 'x' defined but is not a function." in str(e3.value)


def test_compiled_functions_use_safe_builtins_for_imports() -> None:
    # Allowed import inside function should work
    funcs_ok = inj._compile_functions({"h": "def h():\n    import math\n    return math.sqrt(16)"})
    assert funcs_ok["h"]() == 4

    # Disallowed import inside function should raise DisallowedImportError at call time
    funcs_bad = inj._compile_functions({"k": "def k():\n    import os\n    return os.getpid()"})
    with pytest.raises(inj.DisallowedImportError):
        _ = funcs_bad["k"]()


# --------------------------- inject_into_practice --------------------------


def _make_dummy_practice_module(name: str = "practice_mod") -> ModuleType:
    """
    Create a throwaway module with a Practice class and helpers that
    `inject_into_practice` should bind into function globals.
    """
    mod: ModuleType = types.ModuleType(name)

    class Node:  # Helper symbol to be auto-bound
        def __init__(self, value: int) -> None:
            self.value = value

    class Practice:
        # Stubs to test preservation of descriptor semantics
        @staticmethod
        def sstub(a: int) -> int:
            return a + 1

        @classmethod
        def cstub(cls, a: int) -> int:
            return a + 2

        def istub(self, a: int) -> int:
            return a + 3

    setattr(mod, "Node", Node)
    setattr(mod, "Practice", Practice)
    sys.modules[name] = mod
    return mod


def test_inject_into_practice_binds_symbols_and_preserves_descriptors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mod = _make_dummy_practice_module("practice_mod_a")
    Practice = getattr(mod, "Practice")

    # Compile three functions: one uses Node, one intended to replace staticmethod,
    # one intended to replace classmethod, and one replaces instance method.
    sources: dict[str, str] = {
        "make_node_value": "def make_node_value(v):\n    n = Node(v)\n    return n.value",
        "sstub": "def sstub(a):\n    return a * 10",  # should remain staticmethod
        "cstub": "def cstub(cls, a):\n    return a * 100",  # should remain classmethod
        "istub": "def istub(self, a):\n    return a * 1000",  # should remain instance method
    }
    funcs = inj._compile_functions(sources)

    # Also include extra_globals to prove merging
    extra = {"EXTRA": 7}
    inj.inject_into_practice("practice_mod_a", "Practice", funcs, extra_globals=extra)

    # make_node_value should see Node and EXTRA in globals
    fn_make = getattr(Practice, "make_node_value")
    assert fn_make(5) == 5
    assert "Node" in funcs["make_node_value"].__globals__
    assert "EXTRA" in funcs["make_node_value"].__globals__

    # sstub remains staticmethod
    assert isinstance(Practice.__dict__["sstub"], staticmethod)
    assert Practice.sstub(2) == 20

    # cstub remains classmethod
    assert isinstance(Practice.__dict__["cstub"], classmethod)
    assert Practice.cstub(2) == 200

    # istub stays a normal instance method
    p = Practice()
    assert p.istub(2) == 2000
