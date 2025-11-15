from __future__ import annotations

import os

from fastapi import APIRouter

from cs_fundamentals.config import settings
from cs_fundamentals.core.utility import get_app_version
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

router = APIRouter(tags=["Health"])


@router.get("/configz")
def configz() -> dict[str, Any]:
    return {
        "env": settings.env,
        "log_level": settings.log_level,
        "port": settings.port,
        "has_db_url": settings.db_url is not None,  # boolean only
    }


@router.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/version")
def version() -> dict[str, str]:
    return {
        "app": settings.app_name,
        "image-tag": os.getenv("CSF_IMAGE_TAG", "unknown"),
        "version": get_app_version(),
    }
