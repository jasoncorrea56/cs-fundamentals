from __future__ import annotations

import os
import re
from contextlib import suppress
from pathlib import Path

from cs_fundamentals.core.logging_config import get_logger
from cs_fundamentals.models.schemas import PracticeResult, PytestSummary
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

log = get_logger(__name__)


def _find_repo_root(start: Path) -> Path:
    """
    Resolve TEST_ROOT to an absolute path in both environments:
    - in container: /automation (set via Dockerfile ENV)
    - locally: <repo>/automation
    """
    for p in [start, *start.parents]:
        if (p / "pyproject.toml").exists():
            return p
    return start.anchor and Path(start.anchor) or start  # fallback


HERE = Path(__file__).resolve()
REPO_ROOT = _find_repo_root(HERE)
TEST_ROOT = Path(os.getenv("TEST_ROOT", REPO_ROOT / "automation")).resolve()
# Give pytest a hard ceiling so shutdowns don’t hang
TEST_TIMEOUT_SECONDS = int(os.getenv("TEST_TIMEOUT_SECONDS", "30"))

_SUMMARY_KEYS = (
    "passed",
    "failed",
    "errors",
    "skipped",
    "xpassed",
    "xfailed",
    "deselected",
    "warnings",
)


def _parse_pytest_summary(stdout: str) -> dict[str, Any]:
    """
    Parse pytest terminal summary from stdout (works with -q).
    Returns counts + duration when present.
    Parsable Examples:
      "10 passed in 0.23s"
      "9 passed, 1 skipped in 0.45s"
      "8 passed, 1 failed, 1 xfailed in 1.23s"
      "no tests ran in 0.01s" / "no tests collected"
    """
    summary: dict[str, Any] = dict.fromkeys(_SUMMARY_KEYS, 0)
    summary["collected"] = None
    summary["duration_seconds"] = None
    summary["raw"] = stdout.strip()

    # Try to find the last line with counts ("... in 0.xx s")
    lines = stdout.strip().splitlines()
    tail_text = " ".join(lines[-10:]) if lines else ""

    # Duration: "in 0.23s"
    m_dur = re.search(r"\bin\s+([\d.]+)s\b", tail_text)
    if m_dur:
        with suppress(ValueError):
            summary["duration_seconds"] = float(m_dur.group(1))

    # "no tests ran" / "no tests collected"
    if re.search(r"\bno tests (?:ran|collected)\b", tail_text):
        summary["collected"] = 0
        return PytestSummary(**summary)

    # Count tokens like: "8 passed", "1 failed", "2 skipped", "1 xfailed", "1 xpassed", "1 errors", ...
    for key in _SUMMARY_KEYS:
        # Errors sometimes printed as "error" or "errors"
        key_pat = "errors" if key == "errors" else key
        m = re.search(rf"(\d+)\s+{key_pat}\b", tail_text)
        if m:
            summary[key] = int(m.group(1))

    # Best-effort collected estimate (sum of outcomes we know about)
    counted = sum(int(summary[k]) for k in _SUMMARY_KEYS if isinstance(summary[k], int))
    if counted > 0:
        summary["collected"] = counted
    return PytestSummary(**summary)


def _resolve_targets(test_files: list[str] | None) -> list[str]:
    """
    Normalize provided test paths for both container and local runs:
    - Absolute paths: keep as-is
    - Relative paths starting with 'automation/': anchor to '/automation/...'
    - Other relative: resolve under TEST_ROOT
    - None: run entire TEST_ROOT
    """
    if not test_files:
        return [str(TEST_ROOT)]

    targets: list[str] = []
    for raw in test_files:
        p = Path(raw)
        if p.is_absolute():
            targets.append(str(p))
            continue
        s = str(p).lstrip("./")
        if s.startswith("automation/"):
            rel = s[len("automation/") :]  # strip leading 'automation/'
            targets.append(str(TEST_ROOT / rel))
        else:
            targets.append(str(TEST_ROOT / s))
    return targets


def run_pytest(
    test_files: list[str] | None = None,
    test_expr: str | None = None,
) -> dict[str, Any]:
    """
    Run pytest against TEST_ROOT (or specific files) in-process so injected
    functions are visible to the tests.
    """
    # Resolve targets (absolute paths under TEST_ROOT)
    targets = _resolve_targets(test_files)

    # Build pytest CLI args explicitly (no env var bleed)
    args: list[str] = [
        "-q",
        "-p",
        "no:warnings",
        "--basetemp=/tmp/pytest",
        "-o",
        "cache_dir=/tmp/.pytest_cache",
        "-o",
        "asyncio_default_fixture_loop_scope=function",
        *targets,
    ]
    if test_expr:
        args += ["-k", test_expr]

    # Scrub pytest-related env so it doesn't affect other parts (i.e. uvicorn)
    os.environ.pop("PYTEST_ADDOPTS", None)
    os.environ.pop("PYTEST_PLUGINS", None)

    # Portable working dir:
    # - container: /app exists → use it
    # - local: fall back to repo root (where pyproject.toml lives)
    cwd = Path("/app") if Path("/app").exists() else REPO_ROOT

    # Import pytest lazily to avoid importing it in non-test code paths
    import io
    import pytest
    from contextlib import redirect_stdout, redirect_stderr

    out_buf, err_buf = io.StringIO(), io.StringIO()
    prev_cwd = os.getcwd()
    try:
        os.chdir(str(cwd))
        with redirect_stdout(out_buf), redirect_stderr(err_buf):
            exit_code = pytest.main(args)
    finally:
        os.chdir(prev_cwd)

    stdout, stderr = out_buf.getvalue(), err_buf.getvalue()
    result = PracticeResult(
        success=exit_code == 0,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
        summary=_parse_pytest_summary(stdout),
    )
    return result.model_dump()
