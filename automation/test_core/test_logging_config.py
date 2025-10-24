from __future__ import annotations

import io
import json
import logging
import os
import re

import pytest

from cs_fundamentals.core import logging_config as lc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


# ----------------------------- Helpers -----------------------------


def _read_stdout(capsys: pytest.CaptureFixture[str]) -> str:
    out, err = capsys.readouterr()
    # We only write to stdout in these tests
    return out


def _parse_json_lines(text: str) -> list[dict[str, Any]]:
    lines = [ln for ln in (ln.strip() for ln in text.splitlines()) if ln]
    return [json.loads(ln) for ln in lines]


def _clear_root_handlers() -> None:
    root = logging.getLogger()
    for h in root.handlers[:]:
        root.removeHandler(h)


# ----------------------------- Fixtures -----------------------------


@pytest.fixture(autouse=True)
def isolate_logging(monkeypatch: pytest.MonkeyPatch) -> None:  # type: ignore
    """
    Ensure each test starts from a clean root logger and clean env,
    then restore environment afterwards.
    """
    # Clean env that this module reads
    for key in ("LOG_LEVEL", "LOG_FORMAT", "LOG_FILE"):
        monkeypatch.delenv(key, raising=False)

    # Force-configure to a known empty state (also clears handlers)
    _clear_root_handlers()
    logging.getLogger().setLevel(logging.NOTSET)

    yield

    # Best-effort cleanup
    _clear_root_handlers()
    logging.getLogger().setLevel(logging.NOTSET)
    # Reset request_id context var
    token = lc.request_id_var.set(None)
    lc.request_id_var.reset(token)


# -------------------------- RequestIdFilter -------------------------


def test_request_id_filter_injects_attribute_even_when_none() -> None:
    filt = lc.RequestIdFilter()
    record: logging.LogRecord = logging.LogRecord(
        name="x",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="hello",
        args=(),
        exc_info=None,
    )
    # Context default is None
    ok: bool = filt.filter(record)
    assert ok is True
    assert hasattr(record, "request_id")
    assert record.request_id is None  # type: ignore[attr-defined]

    # When context var is set, filter injects that value
    token = lc.request_id_var.set("rid-123")
    try:
        record2: logging.LogRecord = logging.LogRecord(
            name="x",
            level=logging.INFO,
            pathname=__file__,
            lineno=2,
            msg="world",
            args=(),
            exc_info=None,
        )
        assert filt.filter(record2) is True
        assert getattr(record2, "request_id", None) == "rid-123"
    finally:
        lc.request_id_var.reset(token)


# ----------------------------- Formatters ---------------------------


def test_json_formatter_includes_core_fields_and_request_id_and_exc_info(
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Configure root with JSON formatter
    os.environ["LOG_FORMAT"] = "json"
    os.environ["LOG_LEVEL"] = "INFO"
    lc.configure_logging(force=True)

    logger: logging.Logger = lc.get_logger("core.test")
    token = lc.request_id_var.set("abc123")
    try:
        logger.info("hello")
        try:
            raise RuntimeError("boom")
        except RuntimeError:
            logger.exception("failed")
    finally:
        lc.request_id_var.reset(token)

    payloads = _parse_json_lines(_read_stdout(capsys))
    # First line: info with request_id
    p0 = payloads[0]
    assert p0["level"] == "INFO"
    assert p0["logger"] == "core.test"
    assert p0["msg"] == "hello"
    assert "ts" in p0 and "pid" in p0 and "filename" in p0 and "lineno" in p0
    assert p0["request_id"] == "abc123"

    # Second line: exception includes exc_info
    p1 = payloads[1]
    assert p1["level"] == "ERROR"
    assert p1["msg"] == "failed"
    assert "exc_info" in p1 and "RuntimeError: boom" in p1["exc_info"]


def test_console_formatter_output_with_and_without_request_id(
    capsys: pytest.CaptureFixture[str],
) -> None:
    os.environ["LOG_FORMAT"] = "console"
    os.environ["LOG_LEVEL"] = "INFO"
    lc.configure_logging(force=True)

    logger: logging.Logger = lc.get_logger("core.console")

    # Without request id
    logger.info("no rid")
    out1: str = _read_stdout(capsys)
    # Match "... | INFO    | core.console | no rid"
    assert re.search(r"\|\s*INFO\s+\|\s*core\.console\s+\|\s*no rid", out1)

    # With request id
    token = lc.request_id_var.set("rid-xyz")
    try:
        logger.warning("with rid")
        out2: str = _read_stdout(capsys)
        # Don't depend on exact spacing; just verify the important parts
        assert "core.console" in out2
        assert "WARNING" in out2
        assert "rid=rid-xyz" in out2
        assert "with rid" in out2
    finally:
        lc.request_id_var.reset(token)

    # Exception formatting adds stack trace line(s)
    try:
        raise ValueError("bad")
    except ValueError:
        logger.exception("oops")
    out3: str = _read_stdout(capsys)
    assert "oops" in out3 and "ValueError: bad" in out3


# -------------------------- Handler builder -------------------------


def test_build_handler_sets_formatter() -> None:
    fmt = lc.JsonFormatter()
    stream = io.StringIO()
    handler: logging.Handler = lc._build_handler(stream, fmt)
    assert isinstance(handler, logging.StreamHandler)
    assert handler.formatter is fmt


# ------------------------- configure_logging ------------------------


def test_configure_logging_json_writes_to_file_and_stdout(
    tmp_path: pytest.PathLike[str], capsys: pytest.CaptureFixture[str]
) -> None:
    log_file = tmp_path / "app.log"  # type: ignore[operator]
    os.environ["LOG_LEVEL"] = "INFO"
    os.environ["LOG_FORMAT"] = "json"
    os.environ["LOG_FILE"] = str(log_file)

    lc.configure_logging(force=True)
    logger: logging.Logger = lc.get_logger("core.file")

    token = lc.request_id_var.set("file-rid")
    try:
        logger.info("to both")
    finally:
        lc.request_id_var.reset(token)

    # stdout JSON
    out = _read_stdout(capsys)
    payloads = _parse_json_lines(out)
    assert payloads and payloads[0]["logger"] == "core.file"
    assert payloads[0]["request_id"] == "file-rid"

    # file JSON
    content = log_file.read_text(encoding="utf-8")
    file_payloads = _parse_json_lines(content)
    assert file_payloads and file_payloads[0]["msg"] == "to both"
    assert file_payloads[0]["request_id"] == "file-rid"


def test_configure_logging_early_return_when_handlers_exist(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # First configure to JSON INFO
    os.environ["LOG_LEVEL"] = "INFO"
    os.environ["LOG_FORMAT"] = "json"
    lc.configure_logging(force=True)

    # Now change env to console DEBUG, but call without force -> should NO-OP
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["LOG_FORMAT"] = "console"
    lc.configure_logging(force=False)

    logger: logging.Logger = lc.get_logger("core.noop")
    logger.debug("debug-should-NOT-appear")
    logger.info("info-should-appear")

    out = _read_stdout(capsys)
    payloads = _parse_json_lines(out)  # Still JSON due to early return
    # Only one line (INFO), not DEBUG
    assert len(payloads) == 1
    assert payloads[0]["msg"] == "info-should-appear"
    assert payloads[0]["level"] == "INFO"


def test_configure_logging_force_replaces_handlers_and_level(
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Start with JSON INFO
    os.environ["LOG_LEVEL"] = "INFO"
    os.environ["LOG_FORMAT"] = "json"
    lc.configure_logging(force=True)
    logger = lc.get_logger("core.force")
    logger.debug("hidden")
    _ = _read_stdout(capsys)  # Drain

    # Now switch to console DEBUG with force
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["LOG_FORMAT"] = "console"
    lc.configure_logging(force=True)
    logger.debug("now-visible")
    out = _read_stdout(capsys)
    # Be flexible about spaces around columns
    # Search string: " | DEBUG  | core.force | now-visible"
    assert re.search(r"\|\s*DEBUG\s+\|\s*core\.force\s+\|\s*now-visible", out)


# ----------------------------- get_logger ---------------------------


def test_get_logger_returns_named_logger() -> None:
    lg: logging.Logger = lc.get_logger("my.logger")
    assert isinstance(lg, logging.Logger)
    assert lg.name == "my.logger"
