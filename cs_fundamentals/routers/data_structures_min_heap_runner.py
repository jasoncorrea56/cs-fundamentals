from __future__ import annotations

from fastapi import APIRouter

from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001

router = APIRouter(
    prefix="/data-structures/min-heap", tags=["Data Structures - MinHeap Practice"]
)

_submit = make_submit_handler_from_matrix(
    key="ds.minheap",
    success_message="All MinHeap data structure tests executed successfully.",
)


@router.post("/submit")
async def submit_min_heap_practice(payload: MethodsOnly) -> dict:
    return await _submit(payload)
