from pydantic import BaseModel, Field


class PracticeSubmission(BaseModel):
    module: str = Field(..., example="cs_fundamentals.patterns.breadth_first_search")
    class_name: str = Field(..., example="PracticeBreadthFirstSearch")

    # Mapping of method name to full function source (must be a complete `def ...` body)
    methods: dict[str, str]

    # Pytest targeting (Optional)
    test_files: list[str] | None = Field(None, example=["tests/test_bfs.py"])
    test_expr: str | None = Field(None, example="PracticeBreadthFirstSearch and bfs")


class PytestSummary(BaseModel):
    passed: int = 0
    failed: int = 0
    errors: int = 0
    skipped: int = 0
    xpassed: int = 0
    xfailed: int = 0
    deselected: int = 0
    warnings: int = 0
    collected: int | None = None
    duration_seconds: float | None = None
    raw: str = ""


class PracticeResult(BaseModel):
    success: bool
    exit_code: int
    stdout: str
    stderr: str
    summary: PytestSummary | None = None


class MethodsOnly(BaseModel):
    methods: dict[str, str] | None = None
    # Optional per-class override: { "PracticeMinHeap": {...}, "PracticeMaxHeap": {...} }
    class_methods: dict[str, dict[str, str]] | None = None
