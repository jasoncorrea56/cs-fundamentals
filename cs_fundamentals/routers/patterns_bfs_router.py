from __future__ import annotations

from fastapi import APIRouter

from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001

router = APIRouter(prefix="/patterns/bfs", tags=["Patterns - Breadth First Search Practice"])

_submit = make_submit_handler_from_matrix(
    key="patterns.bfs",
    success_message="All Breadth First Search pattern tests executed successfully.",
)


@router.post("/submit")
async def submit_bfs_practice(payload: MethodsOnly) -> dict:
    return await _submit(payload)
