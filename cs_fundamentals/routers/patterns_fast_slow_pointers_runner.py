from __future__ import annotations

from fastapi import APIRouter

from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001

router = APIRouter(
    prefix="/patterns/fast-slow-pointers",
    tags=["Patterns - Fast/Slow Pointers Practice"],
)

_submit = make_submit_handler_from_matrix(
    key="patterns.fast_slow_pointers",
    success_message="All Fast/Slow Pointers pattern tests executed successfully.",
)


@router.post("/submit")
async def submit_fast_slow_pointers_practice(payload: MethodsOnly) -> dict:
    return await _submit(payload)
