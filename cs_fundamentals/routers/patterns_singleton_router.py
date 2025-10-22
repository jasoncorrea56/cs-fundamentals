from __future__ import annotations

from fastapi import APIRouter

from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001

router = APIRouter(prefix="/patterns/singleton", tags=["Patterns - Singleton Practice"])

# Accept method names in a namespaced form, e.g.:
#   "PracticeSingletonClass.__new__": "def __new__(cls): ..."
#   "PracticeBorgSingletonClass.__new__": "def __new__(cls, *args, **kwargs): ..."
# Optional: allow non-namespaced "__new__" to apply to PracticeSingletonClass by default.

TARGET_CLASSES = {
    "PracticeSingletonClass",
    "PracticeSingletonChild",
    "PracticeBorgSingletonClass",
    "PracticeBorgSingletonChild",
    "PracticeBorgSingletonResetChild",
}


def _singleton_splitter(
    methods: dict[str, str],
) -> tuple[dict[str, str], list[tuple[str, str, dict[str, str]]]]:
    """
    Routes methods to the correct Practice* class based on 'ClassName.method' keys.

    Primary injection goes to PracticeSingletonClass; all other classes are injected as extras
    before tests run.
    """
    # Buckets per class
    per_class: dict[str, dict[str, str]] = {cls: {} for cls in TARGET_CLASSES}

    # 1) Parse namespaced keys: "{Class}.{method}"
    remaining: dict[str, str] = {}
    for name, src in methods.items():
        if "." in name:
            cls, meth = name.split(".", 1)
            if cls in per_class:
                per_class[cls][meth] = src
            else:
                # Unknown class qualifier -> treat as normal (will be validated later)
                remaining[name] = src
        else:
            remaining[name] = src

    # 2) If a bare "__new__" is provided, default it to PracticeSingletonClass
    if "__new__" in remaining:
        per_class["PracticeSingletonClass"]["__new__"] = remaining.pop("__new__")

    # 3) Primary methods = those destined for PracticeSingletonClass
    primary = per_class["PracticeSingletonClass"]

    # 4) Extras = other practice classes
    extras: list[tuple[str, str, dict[str, str]]] = []
    module = "cs_fundamentals.patterns.singleton"

    for cls in (
        "PracticeSingletonChild",
        "PracticeBorgSingletonClass",
        "PracticeBorgSingletonChild",
        "PracticeBorgSingletonResetChild",
    ):
        if per_class[cls]:
            extras.append((module, cls, per_class[cls]))

    # If anything is left un-routed (e.g., unknown namespaced target), keep them with primary
    # so validation can raise an informative error later.
    primary |= remaining  # noqa: PIE787

    return primary, extras


# Build the submit handler with the splitter
_submit = make_submit_handler_from_matrix(
    key="patterns.singleton",
    success_message="All singleton tests passed.",
    method_splitter=_singleton_splitter,
)


@router.post("/submit")
async def submit_singleton_practice(payload: MethodsOnly) -> dict:
    return await _submit(payload)
