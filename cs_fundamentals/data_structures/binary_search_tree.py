from __future__ import annotations

import math

from cs_fundamentals.data_structures.binary_tree import BinaryTreeNode


class BinarySearchTree(BinaryTreeNode):
    """
    A binary search tree is a special form of a binary tree that satisfies the binary search properties:
        • The left subtree of a node contains only nodes with keys lesser than the node’s key
        • The right subtree of a node contains only nodes with keys greater than the node’s key
        • The left and right subtree each must also be binary search trees
        • There must be no duplicate nodes
    While traditional traversals (pre/in/post-order) are possible, inorder traversal in BST will be in ascending order.
    Note: Inorder traversal is the most common traversal method of a BST.
    """

    def __init__(
        self,
        value: int = 0,
        left: BinaryTreeNode | None = None,
        right: BinaryTreeNode | None = None,
    ) -> None:
        super().__init__(value, left, right)

    @staticmethod
    def is_valid_bst(root: BinaryTreeNode | None) -> bool:
        if not root:
            return True  # Empty is valid

        stack: list[tuple[BinaryTreeNode, float, float]] = [(root, -math.inf, math.inf)]
        while stack:
            node, lower, upper = stack.pop()
            if node.value <= lower or node.value >= upper:
                return False
            if node.right:
                stack.append((node.right, float(node.value), upper))
            if node.left:
                stack.append((node.left, lower, float(node.value)))
        return True


class PracticeBinarySearchTree(BinaryTreeNode):
    def __init__(
        self,
        value: int = 0,
        left: BinaryTreeNode | None = None,
        right: BinaryTreeNode | None = None,
    ) -> None:
        super().__init__(value, left, right)

    @staticmethod
    def is_valid_bst(root: BinaryTreeNode | None) -> bool:
        raise NotImplementedError
