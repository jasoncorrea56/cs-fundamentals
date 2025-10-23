from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter

from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from typing import Any

router = APIRouter(
    prefix="/data-structures/stack/linked-list",
    tags=["Data Structures - Stack (Linked List) Practice"],
)

_submit: Callable[[MethodsOnly], Awaitable[dict[str, Any]]] = make_submit_handler_from_matrix(
    key="ds.stack.linked_list",
    success_message="All Stack (linked list) data structure tests executed successfully.",
)


@router.post("/submit")
async def submit_stack_linked_list_practice(payload: MethodsOnly) -> dict[str, Any]:
    return await _submit(payload)
