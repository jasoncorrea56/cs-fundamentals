from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix


class MatrixSubmission(BaseModel):
    key: str = Field(..., example="patterns.dfs")
    methods: dict[str, str]


router = APIRouter(prefix="/practice-matrix", tags=["Practice Runner (Matrix)"])


@router.post("/submit")
async def submit_via_matrix(payload: MatrixSubmission) -> dict:
    handler = make_submit_handler_from_matrix(key=payload.key)

    # Re-wrap just the methods for the underlying handler:
    class _Shim(BaseModel):
        methods: dict[str, str]

    return await handler(_Shim(methods=payload.methods))  # type: ignore[arg-type]
