import pytest
from automation.resources.patterns.dfs_data import (
    DFS_PREORDER_OUTPUT,
    DFS_PREORDER_2_OUTPUT,
    DFS_INORDER_OUTPUT,
    DFS_INORDER_2_OUTPUT,
    DFS_POSTORDER_OUTPUT,
    DFS_POSTORDER_2_OUTPUT,
    DFS_LEVEL_AVG_OUTPUT,
)
from patterns.depth_first_search import DepthFirstSearch, Node


class TestDepthFirstSearch:
    @classmethod
    def setup_class(cls) -> None:
        cls.dfs = DepthFirstSearch()

    @pytest.fixture()
    def dfs_root(self) -> Node:
        root = Node(1)
        root.left = Node(2)
        root.right = Node(3)
        root.left.left = Node(4)
        root.left.right = Node(5)
        root.right.left = Node(6)
        root.right.right = Node(7)
        return root

    @pytest.fixture()
    def dfs_root2(self) -> Node:
        root = Node(20)
        root.left = Node(8)
        root.right = Node(22)
        root.left.left = Node(4)
        root.left.right = Node(12)
        root.left.right.left = Node(10)
        root.left.right.right = Node(14)
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

    def test_preorder_dfs(self, dfs_root) -> None:
        result = []
        self.dfs.preorder_dfs(dfs_root, result)
        assert result == DFS_PREORDER_OUTPUT

    def test_preorder_dfs_2(self, dfs_root2) -> None:
        result = []
        self.dfs.preorder_dfs(dfs_root2, result)
        assert result == DFS_PREORDER_2_OUTPUT

    def test_inorder_dfs(self, dfs_root) -> None:
        result = []
        self.dfs.inorder_dfs(dfs_root, result)
        assert result == DFS_INORDER_OUTPUT

    def test_inorder_dfs_2(self, dfs_root2) -> None:
        result = []
        self.dfs.inorder_dfs(dfs_root2, result)
        assert result == DFS_INORDER_2_OUTPUT

    def test_postorder_dfs(self, dfs_root) -> None:
        result = []
        self.dfs.postorder_dfs(dfs_root, result)
        assert result == DFS_POSTORDER_OUTPUT

    def test_postorder_dfs_2(self, dfs_root2) -> None:
        result = []
        self.dfs.postorder_dfs(dfs_root2, result)
        assert result == DFS_POSTORDER_2_OUTPUT

    def test_get_avg_for_each_level(self, level_avg_root) -> None:
        results = self.dfs.get_avg_for_each_level(level_avg_root)
        assert results == DFS_LEVEL_AVG_OUTPUT
