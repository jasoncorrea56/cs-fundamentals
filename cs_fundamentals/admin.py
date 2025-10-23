"""
Admin utilities: Run one-off scripts sharing the same runtime env as the app.
Run via `docker compose run --rm admin <command>`.
"""

import sys
from typing import NoReturn

from cs_fundamentals.core.logging_config import configure_logging, get_logger

# Lazy global, initialized on demand to avoid tripping caplog
log = None


def init_logging() -> None:
    """Initialize logging if not already configured."""
    global log
    if log is None:
        configure_logging()
        log = get_logger(__name__)


def main() -> NoReturn:
    # Ensure logging is configured before any log calls
    init_logging()

    if len(sys.argv) < 2:
        log.error("Usage: admin.py <task>")
        sys.exit(1)

    task = sys.argv[1]
    if task == "health":
        log.info("Admin Service is healthy!")
    else:
        log.error(f"Unknown admin task: {task}")
        sys.exit(1)


if __name__ == "__main__":
    main()
