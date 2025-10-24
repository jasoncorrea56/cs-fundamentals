from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix
from cs_fundamentals.models.schemas import MethodsOnly  # noqa: TC001

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

router = APIRouter(prefix="/patterns/bfs", tags=["Patterns - Breadth First Search Practice"])

_submit: Callable[[MethodsOnly], Awaitable[JSONResponse]] = make_submit_handler_from_matrix(
    key="patterns.bfs",
    success_message="All Breadth First Search pattern tests executed successfully.",
)


@router.post("/submit")
async def submit_bfs_practice(payload: MethodsOnly) -> JSONResponse:
    return await _submit(payload)
