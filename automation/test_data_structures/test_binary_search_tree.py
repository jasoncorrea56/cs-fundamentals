import pytest
from cs_fundamentals.data_structures.binary_search_tree import (
    BinarySearchTree,
    BinaryTreeNode,
)


class TestBinarySearchTree:
    @classmethod
    def setup_class(cls) -> None:
        cls.bst = BinarySearchTree()

    @pytest.fixture()
    def bst_root(self) -> BinaryTreeNode:
        root = BinaryTreeNode(4)
        root.left = BinaryTreeNode(2)
        root.right = BinaryTreeNode(6)
        root.left.left = BinaryTreeNode(1)
        root.left.right = BinaryTreeNode(3)
        root.right.left = BinaryTreeNode(5)
        root.right.right = BinaryTreeNode(7)
        return root

    def test_is_valid_bst(self, bst_root) -> None:
        result = self.bst.is_valid_bst(bst_root)
        assert result is True

    def test_is_valid_bst_true_with_left_and_right_branches(self) -> None:
        #        10
        #       /  \
        #      5    15
        #     / \     \
        #    2   7     20
        root = BinaryTreeNode(
            10,
            left=BinaryTreeNode(5, BinaryTreeNode(2), BinaryTreeNode(7)),
            right=BinaryTreeNode(15, None, BinaryTreeNode(20)),
        )
        assert BinarySearchTree.is_valid_bst(root) is True

    def test_is_valid_bst_false_due_to_bounds_violation(self) -> None:
        # Classic violation: 12 is in the left subtree of 10 but > 10
        #        10
        #       /  \
        #      5    15
        #       \
        #       12   <-- violates BST property
        bad = BinaryTreeNode(
            10,
            left=BinaryTreeNode(5, None, BinaryTreeNode(12)),
            right=BinaryTreeNode(15),
        )
        assert BinarySearchTree.is_valid_bst(bad) is False

    def test_is_valid_bst_empty_is_true(self) -> None:
        assert BinarySearchTree.is_valid_bst(None) is True
