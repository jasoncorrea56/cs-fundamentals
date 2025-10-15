from __future__ import annotations

from fastapi import APIRouter

from cs_fundamentals.core.test_matrix import list_targets

router = APIRouter(prefix="/targets", tags=["Targets"])


@router.get("")
def get_targets() -> list[dict[str, object]]:
    return [
        {
            "key": t.key,
            "kind": t.kind,
            "module": t.module,
            "class_name": t.class_name,
            "test_files": t.test_files,
            "test_expr": t.test_expr,
        }
        for t in list_targets()
    ]
