import pytest
from automation.resources.patterns.bfs_data import BFS_LEVEL_ORDER_OUTPUT, BFS_LEVEL_AVG_OUTPUT
from patterns.breadth_first_search import BreadthFirstSearch, Node


class TestBreadthFirstSearch(object):

    @classmethod
    def setup_class(cls) -> None:
        cls.bfs = BreadthFirstSearch()

    @pytest.fixture()
    def bfs_root(self):
        root = Node(1)
        root.left = Node(2)
        root.right = Node(3)
        root.left.left = Node(4)
        root.left.right = Node(5)
        root.right.left = Node(6)
        root.right.right = Node(7)
        return root

    @pytest.fixture()
    def level_avg_root(self):
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
    def level_avg_output(self):
        return BFS_LEVEL_AVG_OUTPUT

    def test_level_order_bfs(self, bfs_root):
        result = self.bfs.level_order_bfs(bfs_root)
        assert result == BFS_LEVEL_ORDER_OUTPUT

    def test_get_avg_for_each_level(self, level_avg_root, level_avg_output):
        results = self.bfs.get_avg_for_each_level(level_avg_root)
        assert results == level_avg_output
