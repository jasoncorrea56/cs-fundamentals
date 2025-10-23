from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter

from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from typing import Any

router = APIRouter(
    prefix="/data-structures/graph/islands",
    tags=["Data Structures - Graph (Islands II) Practice"],
)


def _split_union_find(
    methods: dict[str, str],
) -> tuple[dict[str, str], list[tuple[str, str, dict[str, str]]]]:
    """
    Split payload methods into:
      - primary methods for PracticeGraphProblems (no dot in name)
      - extra injections for nested PracticeGraphProblems.UnionFind (keys starting with 'UnionFind.')
    Returns: (primary_methods, extra_injections_list)
    Where extra_injections_list = [(module, class_name, methods_dict), ...]
    """
    primary: dict[str, str] = {}
    inner: dict[str, str] = {}

    for name, src in methods.items():
        if name.startswith("UnionFind."):
            inner[name.split(".", 1)[1]] = src
        else:
            primary[name] = src

    extra: list[tuple[str, str, dict[str, str]]] = []
    if inner:
        extra.append(
            (
                "cs_fundamentals.data_structures.graph",
                "PracticeGraphProblems.UnionFind",
                inner,
            )
        )
    return primary, extra


_submit: Callable[[MethodsOnly], Awaitable[dict[str, Any]]] = make_submit_handler_from_matrix(
    key="ds.graph.islands",
    success_message="All Graph Islands II data structure tests executed successfully.",
    method_splitter=_split_union_find,
)


@router.post("/submit")
async def submit_graph_islands_practice(payload: MethodsOnly) -> dict[str, Any]:
    return await _submit(payload)
