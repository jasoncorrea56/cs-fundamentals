from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BinaryTreeNode:
    value: int
    left: BinaryTreeNode | None = None
    right: BinaryTreeNode | None = None


@dataclass(slots=True)
class PracticeBinaryTreeNode:
    value: str
    left: PracticeBinaryTreeNode | None = None
    right: PracticeBinaryTreeNode | None = None
