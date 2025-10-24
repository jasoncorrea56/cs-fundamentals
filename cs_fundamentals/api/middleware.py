from __future__ import annotations

import re
import time
import uuid

import anyio
from fastapi import Request, Response  # noqa: TC002
from starlette.middleware.base import BaseHTTPMiddleware

from cs_fundamentals.core.logging_config import get_logger, request_id_var
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from typing import Any

log = get_logger(__name__)

_TRACEPARENT_RE = re.compile(r"^00-([0-9a-f]{32})-([0-9a-f]{16})-[0-9a-f]{2}$")


class XRequestIDMiddleware(BaseHTTPMiddleware):
    """
    Ensure every request has a stable request_id:
      - Prefer inbound X-Request-ID
      - Else derive from W3C traceparent (span id)
      - Else generate new UUID4
    Propagate it to logs (contextvar) and set X-Request-ID in the response.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        incoming = request.headers.get("x-request-id")
        if not incoming:
            tp = request.headers.get("traceparent")
            if tp:
                m = _TRACEPARENT_RE.match(tp)
                if m:
                    incoming = m.group(2)  # Use the 16-hex span id for brevity
        rid = incoming or uuid.uuid4().hex
        request.state.request_id = rid  # Save for later use by RequestLoggerMiddleware
        token = request_id_var.set(rid)
        try:
            response = await call_next(request)
        finally:
            # Always restore the previous context to avoid leakage across requests
            request_id_var.reset(token)
        response.headers["X-Request-ID"] = rid
        return response


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """
    Structured request/response logger middleware.

    Captures per-request context (method, path, query, remote IP, user-agent, request_id)
    and emits a structured log line on both normal completion and failure.

    Behavior:
      - On each request, measures latency and logs a single "Request" entry at INFO level
        once the response completes.
      - If an exception occurs during request processing, logs at ERROR (with traceback)
        or WARN (if client disconnects prematurely) before re-raising.
      - Integrates with `XRequestIDMiddleware` so all logs share the same `request_id`
        for correlation across distributed traces.

    This middleware is designed to be safe in async contexts, robust under reload,
    and fully compatible with JSON or console logging formats.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """
        Logs every request with latency and status, and still logs cleanly when an exception occurs.
        """
        # Use the request_id propagated by XRequestIDMiddleware (fallback to None)
        # Prefer request.state (set by XRequestID), then contextvar
        req_id = getattr(request.state, "request_id", None) or request_id_var.get()
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
            # Only log completion if we had a response; on exceptions we logged above and re-raise.
            if response is not None:
                extra["duration_ms"] = int((time.perf_counter() - start) * 1000)
                extra["status_code"] = getattr(response, "status_code", 0)
                log.info("Request", extra=extra)

        # No exception => response is set.
        assert response is not None
        return response
