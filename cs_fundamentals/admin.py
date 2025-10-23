"""
Admin utilities: Run one-off scripts sharing the same runtime env as the app.
Run via `docker compose run --rm admin <command>`.
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from cs_fundamentals.core.logging_config import configure_logging, get_logger

if TYPE_CHECKING:
    from logging import Logger


def main(argv: list[str] | None = None) -> None:
    """
    Entry point for admin commands.

    Accepts an optional argv (defaults to sys.argv) to make testing easier.
    """
    if argv is None:
        argv = sys.argv

    # Initialize logging before any log calls.
    configure_logging()
    log: Logger = get_logger(__name__)

    if len(argv) < 2:
        log.error("Usage: admin.py <task>")
        sys.exit(1)

    task = argv[1]
    if task == "health":
        log.info("Admin Service is healthy!")
        return

    log.error(f"Unknown admin task: {task}")
    sys.exit(1)


if __name__ == "__main__":
    main()
