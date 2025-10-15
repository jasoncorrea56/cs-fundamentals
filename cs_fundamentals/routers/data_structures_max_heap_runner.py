from __future__ import annotations

from fastapi import APIRouter

from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001

router = APIRouter(
    prefix="/data-structures/max-heap", tags=["Data Structures - MaxHeap Practice"]
)

_submit = make_submit_handler_from_matrix(
    key="ds.maxheap",
    success_message="All MaxHeap data structure tests executed successfully.",
)


@router.post("/submit")
async def submit_max_heap_practice(payload: MethodsOnly) -> dict:
    return await _submit(payload)
