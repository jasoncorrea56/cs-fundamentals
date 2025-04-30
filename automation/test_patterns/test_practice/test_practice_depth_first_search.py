import pytest
from automation.test_patterns.test_depth_first_search import TestDepthFirstSearch
from patterns.depth_first_search import PracticeDepthFirstSearch


class TestPracticeDepthFirstSearch(TestDepthFirstSearch):
    @classmethod
    def setup_class(cls) -> None:
        cls.dfs = PracticeDepthFirstSearch()

    @pytest.mark.usefixtures("dfs_root")
    def test_preorder_dfs(self, dfs_root) -> None:
        try:
            super().test_preorder_dfs(dfs_root)
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("dfs_root2")
    def test_preorder_dfs_2(self, dfs_root2) -> None:
        try:
            super().test_preorder_dfs_2(dfs_root2)
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("dfs_root")
    def test_inorder_dfs(self, dfs_root) -> None:
        try:
            super().test_inorder_dfs(dfs_root)
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("dfs_root2")
    def test_inorder_dfs_2(self, dfs_root2) -> None:
        try:
            super().test_inorder_dfs_2(dfs_root2)
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("dfs_root")
    def test_postorder_dfs(self, dfs_root) -> None:
        try:
            super().test_postorder_dfs(dfs_root)
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("dfs_root2")
    def test_postorder_dfs_2(self, dfs_root2) -> None:
        try:
            super().test_postorder_dfs_2(dfs_root2)
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("level_avg_root")
    def test_get_avg_for_each_level(self, level_avg_root) -> None:
        try:
            super().test_get_avg_for_each_level(level_avg_root)
        except NotImplementedError:
            assert True
