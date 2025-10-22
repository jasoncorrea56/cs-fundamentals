from __future__ import annotations

from fastapi import APIRouter

from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001

router = APIRouter(prefix="/patterns/dfs", tags=["Patterns - Depth First Search Practice"])

_submit = make_submit_handler_from_matrix(
    key="patterns.dfs",
    success_message="All Depth First Search pattern tests executed successfully.",
)


@router.post("/submit")
async def submit_dfs_practice(payload: MethodsOnly) -> dict:
    return await _submit(payload)
