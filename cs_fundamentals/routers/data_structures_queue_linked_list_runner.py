from __future__ import annotations

from fastapi import APIRouter
from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001

router = APIRouter(
    prefix="/data-structures/queue/linked-list",
    tags=["Data Structures - Queue (Circular Linked List) Practice"],
)

_submit = make_submit_handler_from_matrix(
    key="ds.queue.linked_list",
    success_message="All Queue (Circular Linked List) data structure tests executed successfully.",
)


@router.post("/submit")
async def submit_queue_linked_list_practice(payload: MethodsOnly) -> dict:
    return await _submit(payload)
