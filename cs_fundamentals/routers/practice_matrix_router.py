from __future__ import annotations

from typing import Any, cast, TYPE_CHECKING

from fastapi import APIRouter
from pydantic import BaseModel, Field

from cs_fundamentals.core.handler_factory import make_submit_handler_from_matrix

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


class MatrixSubmission(BaseModel):
    # Pydantic v2: use `examples=[...]`
    key: str = Field(..., examples=["patterns.dfs"])
    methods: dict[str, str]


router = APIRouter(prefix="/practice-matrix", tags=["Practice Runner (Matrix)"])


@router.post("/submit")
async def submit_via_matrix(payload: MatrixSubmission) -> dict[str, Any]:
    # Loosen the param type to `object` so we can pass a local shim class without mypy fights.
    handler = cast(
        "Callable[[object], Awaitable[dict[str, Any]]]",
        make_submit_handler_from_matrix(key=payload.key),
    )

    # Local shim (tests assert the name "_Shim").
    class _Shim(BaseModel):  # noqa: N801  (keep exact name for tests)
        methods: dict[str, str]

    return await handler(_Shim(methods=payload.methods))
