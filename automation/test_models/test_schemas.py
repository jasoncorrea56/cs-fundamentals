from __future__ import annotations

import pytest
from pydantic import ValidationError

from cs_fundamentals.models import schemas


# ---------- PracticeSubmission -------------------------------------------------


def test_practice_submission_required_fields() -> None:
    with pytest.raises(ValidationError) as e:
        schemas.PracticeSubmission()
    msg: str = str(e.value)
    assert "module" in msg
    assert "class_name" in msg
    assert "methods" in msg


def test_practice_submission_accepts_valid_data() -> None:
    payload: dict[str, object] = {
        "module": "cs_fundamentals.patterns.bfs",
        "class_name": "PracticeBreadthFirstSearch",
        "methods": {"bfs": "def bfs(): pass"},
        "test_files": ["tests/test_bfs.py"],
        "test_expr": "PracticeBreadthFirstSearch and bfs",
    }
    ps: schemas.PracticeSubmission = schemas.PracticeSubmission(**payload)
    assert ps.module == payload["module"]
    assert ps.class_name == payload["class_name"]
    assert ps.methods == payload["methods"]
    assert ps.test_files == payload["test_files"]
    assert ps.test_expr == payload["test_expr"]

    # Pull examples directly from the model's JSON schema
    schema: dict = schemas.PracticeSubmission.model_json_schema()
    props: dict = schema.get("properties", {})
    assert props.get("module", {}).get("example") == "cs_fundamentals.patterns.breadth_first_search"
    assert props.get("class_name", {}).get("example") == "PracticeBreadthFirstSearch"


def test_practice_submission_optional_fields_defaults() -> None:
    ps: schemas.PracticeSubmission = schemas.PracticeSubmission(
        module="m", class_name="C", methods={"f": "def f(): pass"}
    )
    assert ps.test_files is None
    assert ps.test_expr is None


# ---------- PytestSummary ------------------------------------------------------


def test_pytest_summary_defaults_and_repr() -> None:
    summary: schemas.PytestSummary = schemas.PytestSummary()
    assert summary.passed == 0
    assert summary.failed == 0
    assert summary.raw == ""
    assert summary.collected is None
    assert summary.duration_seconds is None

    data: dict[str, object] = summary.model_dump()
    assert "passed" in data
    assert isinstance(summary.model_dump_json(), str)


def test_pytest_summary_accepts_values_and_serializes() -> None:
    summary = schemas.PytestSummary(
        passed=3,
        failed=1,
        warnings=2,
        duration_seconds=1.23,
        raw="pytest output",
    )
    dumped: dict[str, object] = summary.model_dump()
    assert dumped["passed"] == 3
    assert dumped["failed"] == 1
    assert "duration_seconds" in dumped
    rehydrated = schemas.PytestSummary(**dumped)
    assert rehydrated == summary


# ---------- PracticeResult -----------------------------------------------------


def test_practice_result_with_summary_serializes_roundtrip() -> None:
    summary: schemas.PytestSummary = schemas.PytestSummary(passed=1, failed=1, raw="raw")
    result: schemas.PracticeResult = schemas.PracticeResult(
        success=True,
        exit_code=0,
        stdout="ok",
        stderr="",
        summary=summary,
    )
    dumped: dict[str, object] = result.model_dump()
    assert dumped["summary"]["passed"] == 1
    json_str: str = result.model_dump_json()
    roundtrip = schemas.PracticeResult.model_validate_json(json_str)
    assert roundtrip == result


def test_practice_result_without_summary() -> None:
    res: schemas.PracticeResult = schemas.PracticeResult(
        success=False,
        exit_code=1,
        stdout="",
        stderr="error",
    )
    assert res.summary is None
    data: dict[str, object] = res.model_dump()
    assert "summary" in data
    assert data["summary"] is None


# ---------- MethodsOnly --------------------------------------------------------


def test_methods_only_defaults_and_optional_fields() -> None:
    mo: schemas.MethodsOnly = schemas.MethodsOnly()
    assert mo.methods is None
    assert mo.class_methods is None

    # Accept nested dicts
    mo2: schemas.MethodsOnly = schemas.MethodsOnly(
        methods={"f": "def f(): pass"},
        class_methods={"PracticeA": {"f": "def f(): pass"}},
    )
    assert isinstance(mo2.methods, dict)
    assert isinstance(mo2.class_methods, dict)


def test_methods_only_json_roundtrip() -> None:
    mo: schemas.MethodsOnly = schemas.MethodsOnly(
        methods={"foo": "def foo(): pass"},
        class_methods={"PracticeBar": {"baz": "def baz(): pass"}},
    )
    serialized: str = mo.model_dump_json()
    parsed: schemas.MethodsOnly = schemas.MethodsOnly.model_validate_json(serialized)
    assert parsed == mo


# ---------- General / misc -----------------------------------------------------


def test_model_json_roundtrip_all_models() -> None:
    """Quick smoke test that all models serialize and deserialize correctly."""
    summary = schemas.PytestSummary(passed=1, failed=2)
    models = [
        schemas.PracticeSubmission(module="m", class_name="C", methods={"f": "def f(): pass"}),
        summary,
        schemas.PracticeResult(success=True, exit_code=0, stdout="out", stderr="", summary=summary),
        schemas.MethodsOnly(methods={"f": "def f(): pass"}),
    ]
    for model in models:
        js: str = model.model_dump_json()
        reloaded = model.__class__.model_validate_json(js)
        assert reloaded == model
        # Validate plain dict equivalence
        assert model.model_dump() == reloaded.model_dump()
