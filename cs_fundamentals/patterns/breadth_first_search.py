from __future__ import annotations

from collections import deque


class Node:
    def __init__(self, value: int) -> None:
        self.value: int = value
        self.left: Node | None = None
        self.right: Node | None = None


def build_tree_level_order(values: list[int | None]) -> Node | None:
    """
    Build a binary tree from a level-order array where None means 'no node' at that position.
    Example: [3,9,20,None,None,15,7]
    """
    if not values:
        return None
    it = iter(values)
    root_val = next(it)
    if root_val is None:
        return None
    root = Node(root_val)
    q: deque[Node] = deque([root])

    for left_val, right_val in zip(it, it):
        parent = q.popleft()
        if left_val is not None:
            parent.left = Node(left_val)
            q.append(parent.left)
        if right_val is not None:
            parent.right = Node(right_val)
            q.append(parent.right)

    # If odd number of remaining values, attach a last left child
    remaining = list(it)
    if remaining:
        parent = q.popleft()
        left_val = remaining[0]
        if left_val is not None:
            parent.left = Node(left_val)
    return root


class BreadthFirstSearch:
    @staticmethod
    def level_order_bfs(root: Node | None) -> list[int]:
        result: list[int] = []
        if not root:
            return result
        q: deque[Node] = deque([root])
        while q:
            node = q.popleft()
            result.append(node.value)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        return result

    @staticmethod
    def get_avg_for_each_level(root: Node | None) -> list[float]:
        """
        Given the root node of a binary tree, return a list containing the average of each level.
        """
        if not root:
            return []
        q: deque[Node] = deque([root])
        avgs: list[float] = []
        while q:
            level_sum = 0
            level_count = len(q)
            for _ in range(level_count):
                node = q.popleft()
                level_sum += node.value
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            avgs.append(level_sum / level_count)
        return avgs


class PracticeBreadthFirstSearch:
    @staticmethod
    def level_order_bfs(root: Node | None) -> list[int]:
        raise NotImplementedError

    @staticmethod
    def get_avg_for_each_level(root: Node | None) -> list[float]:
        raise NotImplementedError
