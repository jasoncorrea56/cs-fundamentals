from __future__ import annotations

import anyio
import time
import uuid
from collections.abc import Awaitable, Callable  # noqa: TC003
from typing import Any

from fastapi import Request, Response  # noqa: TC002
from cs_fundamentals.core.logging_config import get_logger

log = get_logger("api.middleware")


async def request_logger_mw(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    Logs every request with latency and status, and still logs cleanly when an exception occurs.
    """
    req_id = str(uuid.uuid4())
    start = time.perf_counter()
    response: Response | None = None
    extra: dict[str, Any] = {
        "request_id": req_id,
        "method": request.method,
        "path": request.url.path,
        "query": request.url.query,
        "remote": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
    }
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        extra["duration_ms"] = int((time.perf_counter() - start) * 1000)
        if isinstance(exc, anyio.EndOfStream):
            extra["status_code"] = 499
            log.warning("Client disconnected", extra=extra)
        else:
            extra["status_code"] = 500
            log.exception("Request failed", extra=extra)
        raise
    finally:
        if response is not None:
            extra["duration_ms"] = int((time.perf_counter() - start) * 1000)
            extra["status_code"] = getattr(response, "status_code", 0)
            log.info("Request", extra=extra)
