from __future__ import annotations

import traceback

from fastapi import APIRouter, Response

from cs_fundamentals.core.inject import DisallowedImportError
from cs_fundamentals.core.practice_service import run_submission
from cs_fundamentals.core.response import (
    error_response,
    success_response,
    format_pytest_summary_tail,
    is_pytest_ok,
)
from cs_fundamentals.models.schemas import PracticeSubmission  # noqa: TC001

router = APIRouter(prefix="/practice", tags=["Practice Runner"])


@router.post("/submit")
async def submit_practice(payload: PracticeSubmission) -> Response:
    """
    POST /api/v1/practice/submit

    Compile injected methods into the target practice class and run the specified tests.

    Returns:
      - 200 with detailed pytest results on success
      - 400 with stdout/stderr/summary when tests fail or disallowed imports occur
      - 400 with traceback for unexpected exceptions (toggle via PRACTICE_INCLUDE_TRACEBACK)
    """
    try:
        # Run pytest for the provided module/class/methods/tests
        result = run_submission(
            module=payload.module,
            class_name=payload.class_name,
            methods=payload.methods or {},
            test_files=payload.test_files,
            test_expr=payload.test_expr,
        )

        # Canonical success check
        if not is_pytest_ok(result):
            tail = format_pytest_summary_tail(result.get("summary"))
            return error_response(
                status_code=400,
                message=f"Test run failed{tail}. See stdout/stderr for details.",
                # Include both the original submission and the pytest result; response
                # helpers will serialize Pydantic models safely.
                payload={"submission": payload, "result": result},
            )

        # Success path
        return success_response(
            data=result,
            message="All tests executed successfully.",
            # Preserve original behavior: include the incoming submission as metadata
            payload=payload,
        )

    except DisallowedImportError as diexc:
        # Clean handling for sandboxed import violations
        return error_response(
            status_code=400,
            message=str(diexc),
            payload=payload.model_dump(),
        )

    except Exception as exc:  # noqa: BLE001
        # Generic safety net with traceback (controlled by PRACTICE_INCLUDE_TRACEBACK)
        tb = traceback.format_exc()
        return error_response(
            status_code=400,
            message=f"{str(exc)}\n\n{str(tb)}",
            payload=payload.model_dump(),
        )
