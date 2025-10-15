from __future__ import annotations

from fastapi import APIRouter
from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001

router = APIRouter(
    prefix="/data-structures/queue/array",
    tags=["Data Structures - Queue (Circular Array) Practice"],
)

_submit = make_submit_handler_from_matrix(
    key="ds.queue.array",
    success_message="All Queue (Circular Array) data structure tests executed successfully.",
)


@router.post("/submit")
async def submit_queue_array_practice(payload: MethodsOnly) -> dict:
    return await _submit(payload)
