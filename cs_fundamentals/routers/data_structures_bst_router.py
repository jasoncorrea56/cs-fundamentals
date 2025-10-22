from __future__ import annotations

from fastapi import APIRouter

from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001

router = APIRouter(
    prefix="/data-structures/bst",
    tags=["Data Structures - Binary Search Tree Practice"],
)

_submit = make_submit_handler_from_matrix(
    key="ds.bst",
    success_message="All Binary Search Tree data structure tests executed successfully.",
)


@router.post("/submit")
async def submit_bst_practice(payload: MethodsOnly) -> dict:
    return await _submit(payload)
