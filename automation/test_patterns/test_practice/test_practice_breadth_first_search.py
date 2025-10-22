from __future__ import annotations

import pytest
from automation.test_patterns.test_breadth_first_search import TestBreadthFirstSearch
from cs_fundamentals.patterns.breadth_first_search import (
    PracticeBreadthFirstSearch,
    Node,
)


class TestPracticeBreadthFirstSearch(TestBreadthFirstSearch):
    @classmethod
    def setup_class(cls) -> None:
        cls.bfs = PracticeBreadthFirstSearch()

    @pytest.mark.usefixtures("bfs_root")
    def test_level_order_bfs(self, bfs_root: Node) -> None:
        try:
            super().test_level_order_bfs(bfs_root)
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("level_avg_root", "level_avg_output")
    def test_get_avg_for_each_level(
        self, level_avg_root: Node, level_avg_output: list[int]
    ) -> None:
        try:
            super().test_get_avg_for_each_level(level_avg_root, level_avg_output)
        except NotImplementedError:
            assert True

    # ---------- New wrapped method-edge tests ----------

    def test_level_order_bfs_none_returns_empty(self) -> None:
        try:
            # Call through the practice impl directly so we exercise its code path.
            assert self.bfs.level_order_bfs(None) == []
        except NotImplementedError:
            assert True

    def test_get_avg_for_each_level_none_returns_empty(self) -> None:
        try:
            assert self.bfs.get_avg_for_each_level(None) == []
        except NotImplementedError:
            assert True

    def test_get_avg_for_each_level_single_node(self) -> None:
        try:
            root: Node = Node(42)
            assert self.bfs.get_avg_for_each_level(root) == [42.0]
        except NotImplementedError:
            assert True
