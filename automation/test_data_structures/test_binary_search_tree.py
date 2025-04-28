import pytest
from data_structures.binary_search_tree import BinarySearchTree, BinaryTreeNode


class TestBinarySearchTree(object):
    @classmethod
    def setup_class(cls) -> None:
        cls.bst = BinarySearchTree()

    @pytest.fixture()
    def bst_root(self):
        root = BinaryTreeNode(4)
        root.left = BinaryTreeNode(2)
        root.right = BinaryTreeNode(6)
        root.left.left = BinaryTreeNode(1)
        root.left.right = BinaryTreeNode(3)
        root.right.left = BinaryTreeNode(5)
        root.right.right = BinaryTreeNode(7)
        return root

    def test_is_valid_bst(self, bst_root):
        result = self.bst.is_valid_bst(bst_root)
        assert result is True
