from __future__ import annotations

import logging
import re
import uuid
from collections.abc import Callable  # noqa: TC003
from typing import Any, TypedDict, cast

import anyio
import pytest
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.testclient import TestClient

import cs_fundamentals.api.middleware as mw
from cs_fundamentals.core.logging_config import request_id_var


class CapturedCall(TypedDict, total=False):
    level: int
    msg: str
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    extra: dict[str, Any]


class CallSink:
    """Stores extra dicts and call metadata for log invocations."""

    def __init__(self) -> None:
        self.calls: list[CapturedCall] = []

    def record(self, level: int, msg: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> None:
        self.calls.append(
            CapturedCall(
                level=level,
                msg=msg,
                args=args,
                kwargs=kwargs,
                extra=cast("dict[str, Any]", kwargs.get("extra", {})),
            )
        )

    # Convenience helper
    def find(self, msg_substr: str) -> CapturedCall | None:
        for c in self.calls:
            if msg_substr in c["msg"]:
                return c
        return None


HEX32 = re.compile(r"^[0-9a-f]{32}$")


def make_app() -> FastAPI:
    app: FastAPI = FastAPI()

    # Add RequestLogger first, then XRequestID last (the last added runs first/outermost)
    app.add_middleware(mw.RequestLoggerMiddleware)
    app.add_middleware(mw.XRequestIDMiddleware)

    @app.get("/echo")
    def echo(request: Request) -> JSONResponse:
        return JSONResponse(
            {
                "state_request_id": getattr(request.state, "request_id", None),
                "ctx_request_id": request_id_var.get(),
            }
        )

    @app.get("/ok")
    def ok() -> PlainTextResponse:
        return PlainTextResponse("ok", status_code=200)

    @app.get("/boom")
    def boom() -> PlainTextResponse:  # Never returns, but keeps linter happy
        raise ValueError("kaboom")

    @app.get("/disconnect")
    def disconnect() -> PlainTextResponse:  # Never returns
        raise anyio.EndOfStream()

    return app


@pytest.fixture
def sink() -> CallSink:
    return CallSink()


@pytest.fixture(autouse=True)
def patch_logger(monkeypatch: pytest.MonkeyPatch, sink: CallSink) -> logging.Logger:
    """
    Replace the module-level logger with a stdlib logger, and shim its
    info/warning/exception to capture `extra` at the call site *and* forward
    to the real logger so caplog still receives records.
    """
    logger: logging.Logger = logging.getLogger("test.middleware")
    logger.setLevel(logging.DEBUG)
    logger.propagate = True

    # Attach before app is constructed
    monkeypatch.setattr(mw, "log", logger, raising=True)

    # Preserve originals
    orig_info: Callable[..., Any] = logger.info
    orig_warning: Callable[..., Any] = logger.warning
    orig_exception: Callable[..., Any] = logger.exception

    def wrap(orig: Callable[..., Any], level: int) -> Callable[..., Any]:
        def _inner(msg: str, *args: Any, **kwargs: Any) -> Any:
            sink.record(level, msg, args, kwargs)
            return orig(msg, *args, **kwargs)

        return _inner

    # Patch bound methods (keep type: ignore for mypy on bound patching)
    monkeypatch.setattr(logger, "info", wrap(orig_info, logging.INFO))
    monkeypatch.setattr(logger, "warning", wrap(orig_warning, logging.WARNING))
    monkeypatch.setattr(logger, "exception", wrap(orig_exception, logging.ERROR))

    return logger


@pytest.fixture
def client(patch_logger: logging.Logger) -> TestClient:
    # Ensure logger is patched before app creation
    app: FastAPI = make_app()
    return TestClient(app, raise_server_exceptions=False)


def _find_record(caplog: pytest.LogCaptureFixture, msg_substr: str) -> logging.LogRecord | None:
    for rec in caplog.records:
        if msg_substr in rec.getMessage():
            return rec
    return None


def test_x_request_id_uses_incoming_header_and_sets_response_and_state_and_ctx(
    client: TestClient,
) -> None:
    rid: str = uuid.uuid4().hex
    resp = client.get("/echo", headers={"X-Request-ID": rid, "User-Agent": "pytest"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["state_request_id"] == rid
    assert data["ctx_request_id"] == rid

    resp2 = client.get("/ok", headers={"X-Request-ID": rid})
    assert resp2.headers.get("X-Request-ID") == rid


def test_x_request_id_uses_traceparent_span_id_when_present(client: TestClient) -> None:
    trace_id: str = "0" * 32
    span_id: str = "a1b2c3d4e5f6a7b8"
    tp: str = f"00-{trace_id}-{span_id}-01"

    resp = client.get("/echo", headers={"traceparent": tp})
    assert resp.status_code == 200
    data = resp.json()
    assert data["state_request_id"] == span_id
    assert data["ctx_request_id"] == span_id

    resp2 = client.get("/ok", headers={"traceparent": tp})
    assert resp2.headers.get("X-Request-ID") == span_id


def test_x_request_id_generates_uuid_when_missing(client: TestClient) -> None:
    resp = client.get("/echo")
    assert resp.status_code == 200
    data = resp.json()
    rid: str = data["state_request_id"]
    assert isinstance(rid, str) and HEX32.match(rid)
    assert data["ctx_request_id"] == rid

    resp2 = client.get("/ok")
    assert HEX32.match(resp2.headers.get("X-Request-ID", ""))


def test_contextvar_is_reset_between_requests(client: TestClient) -> None:
    rid1: str = "1" * 32
    resp1 = client.get("/echo", headers={"X-Request-ID": rid1})
    d1 = resp1.json()
    assert d1["state_request_id"] == rid1
    assert d1["ctx_request_id"] == rid1

    resp2 = client.get("/echo")
    d2 = resp2.json()
    rid2: str = d2["state_request_id"]
    assert HEX32.match(rid2)
    assert rid2 != rid1
    assert d2["ctx_request_id"] == rid2


def test_request_logger_logs_info_on_success(
    client: TestClient, caplog: pytest.LogCaptureFixture, sink: CallSink
) -> None:
    caplog.set_level(logging.INFO)
    rid: str = "2" * 32

    r = client.get("/ok?x=1", headers={"X-Request-ID": rid, "User-Agent": "pytest/ua"})
    assert r.status_code == 200

    # Still assert visible log
    rec = _find_record(caplog, "Request")
    assert rec is not None
    assert rec.levelno == logging.INFO

    # Assert call-site extras captured
    captured = cast("CapturedCall", sink.find("Request"))
    assert captured is not None
    extra = captured["extra"]
    assert extra["request_id"] == rid
    assert extra["method"] == "GET"
    assert extra["path"] == "/ok"
    assert extra["query"] == "x=1"
    assert extra["status_code"] == 200
    assert isinstance(extra["duration_ms"], int)


def test_request_logger_logs_error_and_re_raises_on_exception(
    client: TestClient, caplog: pytest.LogCaptureFixture, sink: CallSink
) -> None:
    caplog.set_level(logging.DEBUG)
    rid: str = "3" * 32

    r = client.get("/boom", headers={"X-Request-ID": rid})
    assert r.status_code == 500

    rec = _find_record(caplog, "Request failed")
    assert rec is not None
    assert rec.levelno == logging.ERROR

    captured = cast("CapturedCall", sink.find("Request failed"))
    assert captured is not None
    extra = captured["extra"]
    assert extra["request_id"] == rid
    assert extra["status_code"] == 500
    assert isinstance(extra["duration_ms"], int)


def test_request_logger_warns_on_client_disconnect(
    client: TestClient, caplog: pytest.LogCaptureFixture, sink: CallSink
) -> None:
    caplog.set_level(logging.DEBUG)
    rid: str = "4" * 32

    r = client.get("/disconnect", headers={"X-Request-ID": rid})
    assert r.status_code == 500  # Re-raised; framework renders 500

    rec = _find_record(caplog, "Client disconnected")
    assert rec is not None
    assert rec.levelno == logging.WARNING

    captured = cast("CapturedCall", sink.find("Client disconnected"))
    assert captured is not None
    extra = captured["extra"]
    assert extra["request_id"] == rid
    assert extra["status_code"] == 499
    assert isinstance(extra["duration_ms"], int)
