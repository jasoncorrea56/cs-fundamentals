from __future__ import annotations

from fastapi import APIRouter

from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001

router = APIRouter(
    prefix="/data-structures/linked-list-single",
    tags=["Data Structures - Singly Linked List Practice"],
)

_submit = make_submit_handler_from_matrix(
    key="ds.linked_list_single",
    success_message="All Singly Linked List data structure tests executed successfully.",
)


@router.post("/submit")
async def submit_single_linked_list_practice(payload: MethodsOnly) -> dict:
    return await _submit(payload)
