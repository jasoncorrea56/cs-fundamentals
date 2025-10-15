from __future__ import annotations


class Node:
    def __init__(self, value: int) -> None:
        self.value: int = value
        self.left: Node | None = None
        self.right: Node | None = None


class DepthFirstSearch:
    @staticmethod
    def preorder_dfs(node: Node | None, data: list[int]) -> None:
        if not node:
            return None

        data.append(node.value)
        DepthFirstSearch.preorder_dfs(node.left, data)
        DepthFirstSearch.preorder_dfs(node.right, data)
        return

    @staticmethod
    def inorder_dfs(node: Node | None, data: list[int]) -> None:
        if not node:
            return None

        DepthFirstSearch.inorder_dfs(node.left, data)
        data.append(node.value)
        DepthFirstSearch.inorder_dfs(node.right, data)
        return

    @staticmethod
    def postorder_dfs(node: Node | None, data: list[int]) -> None:
        if not node:
            return None

        DepthFirstSearch.postorder_dfs(node.left, data)
        DepthFirstSearch.postorder_dfs(node.right, data)
        data.append(node.value)
        return

    @staticmethod
    def get_avg_for_each_level(root: Node | None) -> list[float]:
        """
        Given the root node of a binary tree, return a list containing the average of each level.
        :param root: Root node of binary tree
        :return: List of averages for each level
        """
        if not root:
            return []

        data: dict[int, tuple[int, int]] = {}

        def preorder_dfs(node: Node | None, level: int = 0) -> None:
            if not node:
                return None

            if level not in data:
                data[level] = (node.value, 1)
            else:
                v, c = data[level]
                v += node.value
                c += 1
                data[level] = (v, c)

            preorder_dfs(node.left, level + 1)
            preorder_dfs(node.right, level + 1)
            return

        preorder_dfs(root)
        result: list[float] = []
        i = 0
        while i in data:
            val, count = data[i]
            result.append(val / count)
            i += 1
        return result


class PracticeDepthFirstSearch:
    @staticmethod
    def preorder_dfs(node: Node | None, data: list[int]) -> None:
        raise NotImplementedError

    @staticmethod
    def inorder_dfs(node: Node | None, data: list[int]) -> None:
        raise NotImplementedError

    @staticmethod
    def postorder_dfs(node: Node | None, data: list[int]) -> None:
        raise NotImplementedError

    @staticmethod
    def get_avg_for_each_level(root: Node | None) -> list[float]:
        """
        Given the root node of a binary tree, return a list containing the average of each level.
        :param root: Root node of binary tree
        :return: List of averages for each level
        """
        raise NotImplementedError
