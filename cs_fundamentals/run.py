from __future__ import annotations

from typing import Any, cast

import uvicorn

from cs_fundamentals.config import settings

# Prefer a dedicated setup function if present, but don't require it.
try:
    from cs_fundamentals.core.logging_config import setup_logging as _setup_logging  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    _setup_logging = None


def _init_logging() -> dict[str, Any]:
    """
    Return a dictConfig for Uvicorn logging.

    - If a project-level `setup_logging(name)` exists, use it.
    - Otherwise, provide a minimal default dictConfig so tests (and dev runs)
      still pass a dict for `log_config`.
    """
    if _setup_logging is not None:
        cfg = _setup_logging("cs_fundamentals")
        # Be explicit for mypy: factory may be untyped.
        if isinstance(cfg, dict):
            return cast("dict[str, Any]", cfg)

    # Minimal fallback config
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {},
        "loggers": {},
    }


if __name__ == "__main__":
    uvicorn.run(
        "cs_fundamentals.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True,
        log_config=_init_logging(),
        log_level=settings.log_level.lower(),
        access_log=False,
    )
