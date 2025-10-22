from __future__ import annotations

from cs_fundamentals.data_structures.binary_tree import (
    BinaryTreeNode,
    PracticeBinaryTreeNode,
)


def test_binary_tree_node_defaults_and_fields() -> None:
    """Default left/right should be None and fields should be assigned."""
    n: BinaryTreeNode = BinaryTreeNode(1)
    assert n.value == 1
    assert n.left is None
    assert n.right is None


def test_binary_tree_node_with_children() -> None:
    """Children should be assigned and reachable via left/right."""
    left: BinaryTreeNode = BinaryTreeNode(2)
    right: BinaryTreeNode = BinaryTreeNode(3)
    root: BinaryTreeNode = BinaryTreeNode(1, left=left, right=right)

    assert root.left is left
    assert root.right is right
    assert root.left.value == 2
    assert root.right.value == 3


def test_practice_binary_tree_node_defaults_and_fields() -> None:
    """PracticeBinaryTreeNode mirrors BinaryTreeNode behavior (defaults and assignment)."""
    n: PracticeBinaryTreeNode = PracticeBinaryTreeNode("x")
    assert n.value == "x"
    assert n.left is None
    assert n.right is None


def test_practice_binary_tree_node_with_children() -> None:
    """PracticeBinaryTreeNode supports children on construction."""
    left_node: PracticeBinaryTreeNode = PracticeBinaryTreeNode("L")
    right_node: PracticeBinaryTreeNode = PracticeBinaryTreeNode("R")
    root: PracticeBinaryTreeNode = PracticeBinaryTreeNode("root", left=left_node, right=right_node)

    assert root.left is left_node
    assert root.right is right_node
    assert root.left.value == "L"
    assert root.right.value == "R"
