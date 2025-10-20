"""
Admin utilities: Run one-off scripts sharing the same runtime env as the app.
Run via `docker compose run --rm admin <command>`.
"""

import sys

# import logging
from cs_fundamentals.core.logging_config import configure_logging, get_logger

configure_logging()
log = get_logger(__name__)


def main() -> None:
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
