from __future__ import annotations

from fastapi import APIRouter

from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001

router = APIRouter(
    prefix="/patterns/sliding-window", tags=["Patterns - Sliding Window Practice"]
)

_submit = make_submit_handler_from_matrix(
    key="patterns.sliding_window",
    success_message="All Sliding Window pattern tests executed successfully.",
)


@router.post("/submit")
async def submit_sliding_window_practice(payload: MethodsOnly) -> dict:
    return await _submit(payload)
