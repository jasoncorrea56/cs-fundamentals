from __future__ import annotations

import os

import uvicorn

from cs_fundamentals.config import settings
from cs_fundamentals.core.logging_config import configure_logging, get_logger


def main() -> None:
    # Configure our logging once; disable Uvicorn's dictConfig below.
    configure_logging(force=True)
    log = get_logger(__name__)
    log.info("event=runner.startup", extra={"host": "0.0.0.0", "port": settings.port})

    uvicorn.run(
        "cs_fundamentals.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True,
        # Disable Uvicorn's logging config so ours stays in control.
        log_config=None,
        # We'll keep access logs off (toggle via env if you like).
        access_log=os.getenv("UVICORN_ACCESS_LOG", "0") not in {"0", "false", "False"},
    )


if __name__ == "__main__":
    main()
