from __future__ import annotations

import pytest

from cs_fundamentals.core import test_matrix as tm


def test_get_target_known_key_returns_dataclass() -> None:
    target: tm.TestTarget = tm.get_target("patterns.bfs")
    # Basic shape checks
    assert isinstance(target, tm.TestTarget)
    assert target.key == "patterns.bfs"
    assert isinstance(target.module, str) and target.module
    assert isinstance(target.class_name, str | list)
    assert isinstance(target.test_files, list) and len(target.test_files) > 0
    assert isinstance(target.test_expr, str) and target.test_expr
    assert target.kind in {"pattern", "data-structure"}


def test_get_target_unknown_key_raises_informative_error() -> None:
    with pytest.raises(KeyError) as excinfo:
        tm.get_target("nope.not_here")
    msg: str = str(excinfo.value)
    # Should include the unknown key and suggest available keys
    assert "Unknown target 'nope.not_here'" in msg
    # Must list at least one known key from MATRIX
    for known in tm.MATRIX:
        if known in msg:
            break
    else:
        pytest.fail("Error message did not include any known keys from MATRIX")


def test_list_targets_returns_all_sorted_by_key() -> None:
    items: list[tm.TestTarget] = tm.list_targets()
    # Sorted by key ascending
    keys: list[str] = [t.key for t in items]
    assert keys == sorted(keys)
    # Count matches underlying matrix
    assert len(items) == len(tm.MATRIX)
    # Every returned item should be exactly the object from MATRIX
    for t in items:
        assert tm.MATRIX[t.key] is t


def test_list_targets_filters_by_kind_and_is_sorted() -> None:
    for kind in ("pattern", "data-structure"):
        filtered: list[tm.TestTarget] = tm.list_targets(kind=kind)
        assert all(t.kind == kind for t in filtered)
        keys: list[str] = [t.key for t in filtered]
        assert keys == sorted(keys)
        # Should be a proper subset of the full list
        assert 0 < len(filtered) <= len(tm.MATRIX)


def test_matrix_entries_have_consistent_shape() -> None:
    for key, t in tm.MATRIX.items():
        # Key in struct should match the dict key
        assert t.key == key
        # Test files should be non-empty strings pointing under automation/
        assert isinstance(t.test_files, list) and all(
            isinstance(p, str) and p for p in t.test_files
        )
        assert any(p.startswith("automation/") for p in t.test_files)
        # Test expression should be present
        assert isinstance(t.test_expr, str) and t.test_expr
        # Module path should look like a dotted module
        assert "." in t.module
        # Kind must be one of the supported values
        assert t.kind in {"pattern", "data-structure"}
