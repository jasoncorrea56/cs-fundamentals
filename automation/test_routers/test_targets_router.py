from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cs_fundamentals.routers import targets_router as tg


@pytest.fixture()
def app() -> FastAPI:
    """Mount the router into a minimal FastAPI app."""
    app: FastAPI = FastAPI()
    app.include_router(tg.router)
    return app


def test_router_registration(app: FastAPI) -> None:
    """Router should expose the expected prefix, tag, and path."""
    routes: set[str] = {r.path for r in app.router.routes}
    assert "/targets" in routes or "" in routes  # FastAPI normalizes "" to "/targets"
    assert tg.router.prefix == "/targets"
    assert any("Targets" in t for t in tg.router.tags)


def test_get_targets_returns_mapped_dicts(monkeypatch: pytest.MonkeyPatch) -> None:
    """get_targets should map list_targets() objects to plain dicts with expected keys."""
    fake_items: list[Any] = [
        SimpleNamespace(
            key="patterns.bfs",
            kind="pattern",
            module="cs_fundamentals.patterns.breadth_first_search",
            class_name="PracticeBreadthFirstSearch",
            test_files=["automation/test_patterns/test_breadth_first_search.py"],
            test_expr="breadth_first_search or PracticeBreadthFirstSearch",
        ),
        SimpleNamespace(
            key="ds.maxheap",
            kind="data-structure",
            module="cs_fundamentals.data_structures.maxheap",
            class_name="PracticeMaxHeap",
            test_files=["automation/test_data_structures/test_heap.py"],
            test_expr="MaxHeap or PracticeMaxHeap",
        ),
    ]

    monkeypatch.setattr(tg, "list_targets", lambda kind=None: fake_items)

    out: list[dict[str, object]] = tg.get_targets()
    assert isinstance(out, list)
    assert len(out) == 2

    first: dict[str, object] = out[0]
    assert first["key"] == "patterns.bfs"
    assert first["kind"] == "pattern"
    assert first["module"] == "cs_fundamentals.patterns.breadth_first_search"
    assert first["class_name"] == "PracticeBreadthFirstSearch"
    assert first["test_files"] == ["automation/test_patterns/test_breadth_first_search.py"]
    assert "test_expr" in first


def test_get_targets_through_http(app: FastAPI, monkeypatch: pytest.MonkeyPatch) -> None:
    """End-to-end HTTP check to ensure route wiring works and output shape is correct."""
    client: TestClient = TestClient(app)

    fake_items: list[Any] = [
        SimpleNamespace(
            key="patterns.sorting",
            kind="pattern",
            module="cs_fundamentals.patterns.sorting",
            class_name="PracticeSortingAlgorithms",
            test_files=["automation/test_patterns/test_sorting.py"],
            test_expr="SortingAlgorithms or PracticeSortingAlgorithms",
        )
    ]
    monkeypatch.setattr(tg, "list_targets", lambda kind=None: fake_items)

    resp = client.get("/targets")
    assert resp.status_code == 200
    payload: list[dict[str, object]] = resp.json()
    assert payload == [
        {
            "key": "patterns.sorting",
            "kind": "pattern",
            "module": "cs_fundamentals.patterns.sorting",
            "class_name": "PracticeSortingAlgorithms",
            "test_files": ["automation/test_patterns/test_sorting.py"],
            "test_expr": "SortingAlgorithms or PracticeSortingAlgorithms",
        }
    ]
