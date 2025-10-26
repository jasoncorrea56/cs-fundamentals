from __future__ import annotations

import pytest
from automation.resources.patterns.bfs_data import (
    BFS_LEVEL_ORDER_OUTPUT,
    BFS_LEVEL_AVG_OUTPUT,
)
from cs_fundamentals.patterns.breadth_first_search import (
    BreadthFirstSearch,
    Node,
    build_tree_level_order,
)


class TestBreadthFirstSearch:
    @classmethod
    def setup_class(cls) -> None:
        cls.bfs = BreadthFirstSearch()

    @pytest.fixture()
    def bfs_root(self) -> Node:
        root = Node(1)
        root.left = Node(2)
        root.right = Node(3)
        root.left.left = Node(4)
        root.left.right = Node(5)
        root.right.left = Node(6)
        root.right.right = Node(7)
        return root

    @pytest.fixture()
    def level_avg_root(self) -> Node:
        root = Node(4)
        root.left = Node(7)
        root.left.left = Node(10)
        root.left.right = Node(2)
        root.left.right.right = Node(6)
        root.left.right.right.left = Node(2)
        root.right = Node(9)
        root.right.right = Node(6)
        return root

    @pytest.fixture()
    def level_avg_output(self) -> list[int]:
        return BFS_LEVEL_AVG_OUTPUT

    def test_level_order_bfs(self, bfs_root: Node) -> None:
        result = self.bfs.level_order_bfs(bfs_root)
        assert result == BFS_LEVEL_ORDER_OUTPUT

    def test_get_avg_for_each_level(
        self, level_avg_root: Node, level_avg_output: list[int]
    ) -> None:
        results = self.bfs.get_avg_for_each_level(level_avg_root)
        assert results == level_avg_output


# ---------- Helpers ----------


def _collect_level_order(root: Node | None) -> list[int]:
    """Helper to validate built trees using the real BFS implementation."""
    return BreadthFirstSearch.level_order_bfs(root)


# ---------- Free-function and edge-case tests (module-level) ----------


def test_build_tree_level_order_empty_and_root_none() -> None:
    """build_tree_level_order should return None for empty input and [None] root."""
    assert build_tree_level_order([]) is None
    assert build_tree_level_order([None]) is None


def test_build_tree_level_order_full_and_odd_tail() -> None:
    """
    Ensure nodes are attached correctly and the “odd remainder” path is covered.

    Example:
      Values = [1, 2, 3, 4]
      Level Order: [1, 2, 3, 4]
      Expected tree:
          1
         / \
        2   3
       /
      4
    """
    root: Node | None = build_tree_level_order([1, 2, 3, 4])
    assert isinstance(root, Node)
    assert _collect_level_order(root) == [1, 2, 3, 4]

    # Also cover a full first level then a partial second level.
    root2: Node | None = build_tree_level_order([10, 20, 30, 40, 50])
    assert isinstance(root2, Node)
    # Structure:
    #     10
    #    /  \
    #  20    30
    #  / \
    # 40 50
    assert _collect_level_order(root2) == [10, 20, 30, 40, 50]


def test_level_order_bfs_none_returns_empty() -> None:
    """BreadthFirstSearch.level_order_bfs should return [] when root is None."""
    assert BreadthFirstSearch.level_order_bfs(None) == []


def test_get_avg_for_each_level_none_returns_empty() -> None:
    """BreadthFirstSearch.get_avg_for_each_level should return [] when root is None."""
    assert BreadthFirstSearch.get_avg_for_each_level(None) == []


def test_get_avg_for_each_level_single_node() -> None:
    """Averages for a single-node tree is just [value]."""
    root: Node = Node(42)
    assert BreadthFirstSearch.get_avg_for_each_level(root) == [42.0]
