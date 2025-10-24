import os
import tomllib
from importlib.metadata import version as get_version, PackageNotFoundError
from pathlib import Path
from typing import Any


def get_app_version() -> Any:
    try:
        return get_version("cs-fundamentals")
    except PackageNotFoundError:
        try:
            with open(Path(__file__).parents[1] / "pyproject.toml", "rb") as f:
                return tomllib.load(f)["project"]["version"]
        except Exception:
            return os.getenv("APP_VERSION", "dev")
