from __future__ import annotations

import traceback

from fastapi import APIRouter

from cs_fundamentals.core.inject import DisallowedImportError
from cs_fundamentals.core.practice_service import run_submission
from cs_fundamentals.core.response import error_response, success_response
from cs_fundamentals.models.schemas import PracticeSubmission  # noqa: TC001

router = APIRouter(prefix="/practice", tags=["Practice Runner"])


@router.post("/submit")
async def submit_practice(payload: PracticeSubmission) -> dict:
    """
    POST /api/v1/practice/submit
    body: PracticeSubmission { module, class_name, methods, test_files?, test_expr? }
    """
    try:
        result = run_submission(
            module=payload.module,
            class_name=payload.class_name,
            methods=payload.methods,
            test_files=payload.test_files,
            test_expr=payload.test_expr,
        )

        return success_response(
            data=result,
            message="All tests executed successfully.",
            payload=payload,
        )

    except DisallowedImportError as diexc:
        return error_response(
            status_code=400,
            message=str(diexc),
            payload=payload,
        )

    except Exception as exc:  # noqa: BLE001
        tb = traceback.format_exc()
        return error_response(
            status_code=400,
            message=f"{str(exc)}\n\n{str(tb)}",
            payload=payload,
        )
