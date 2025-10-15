from __future__ import annotations

import io
import os
import pytest
import re
import sys
from contextlib import redirect_stderr, redirect_stdout, suppress
from pathlib import Path
from typing import Any

from cs_fundamentals.models.schemas import PracticeResult, PytestSummary


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
    tail = stdout.strip().splitlines()[-10:]  # look at last ~10 lines, just in case
    tail_text = " ".join(tail)

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
    summary["collected"] = counted if counted > 0 else summary["collected"]

    return PytestSummary(**summary)


def run_pytest(
    test_files: list[str] | None = None,
    test_expr: str | None = None,
) -> dict[str, Any]:
    """
    Run pytest against automation/ or a given file list and capture output.
    Returns a serialized PracticeResult (dict) with a parsed `summary`.
    """
    repo_root = Path(__file__).resolve().parents[2]
    automation_dir = repo_root / "automation"

    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    args: list[str] = []

    # args.append("-v")

    if test_files:
        args.extend(test_files)
    else:
        args.append(str(automation_dir))

    if test_expr:
        args.extend(["-k", test_expr])

    out_buf, err_buf = io.StringIO(), io.StringIO()
    cwd = os.getcwd()

    try:
        os.chdir(repo_root)
        with redirect_stdout(out_buf), redirect_stderr(err_buf):
            exit_code = pytest.main(args)
    finally:
        os.chdir(cwd)

    stdout = out_buf.getvalue()
    stderr = err_buf.getvalue()

    result = PracticeResult(
        success=exit_code == 0,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
        summary=_parse_pytest_summary(stdout),
    )

    return result.model_dump()
