import pytest
from automation.test_patterns.test_breadth_first_search import TestBreadthFirstSearch
from patterns.breadth_first_search import PracticeBreadthFirstSearch


class TestPracticeBreadthFirstSearch(TestBreadthFirstSearch):
    @classmethod
    def setup_class(cls) -> None:
        cls.bfs = PracticeBreadthFirstSearch()

    @pytest.mark.usefixtures("bfs_root")
    def test_level_order_bfs(self, bfs_root):
        try:
            super().test_level_order_bfs(bfs_root)
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("level_avg_root", "level_avg_output")
    def test_get_avg_for_each_level(self, level_avg_root, level_avg_output):
        try:
            super().test_get_avg_for_each_level(level_avg_root, level_avg_output)
        except NotImplementedError:
            assert True
