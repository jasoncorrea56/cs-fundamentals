from collections import deque


class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BreadthFirstSearch(object):
    @staticmethod
    def level_order_bfs(root: Node):
        result = []
        if not root:
            return result

        queue = deque()
        queue.append(root)
        while queue:
            # current_level = []
            for _ in range(len(queue)):
                current_node = queue.popleft()
                # current_level.append(current_node.value)
                result.append(current_node.value)
                if current_node.left:
                    queue.append(current_node.left)
                if current_node.right:
                    queue.append(current_node.right)

            # result.append(current_level)

        return result

    @staticmethod
    def get_avg_for_each_level(root: Node) -> list[int]:
        """
        Given the root node of a binary tree, return a list containing the average of each level.
        :param root: Root node of binary tree
        :return: List of averages for each level
        """

        def bfs(node):
            if not node:
                return None

            level = 0
            queue = deque()
            queue.append(node)
            while queue:
                level += 1
                size = len(queue)
                for _ in range(size):
                    curr = queue.popleft()
                    if level not in data:
                        data[level] = (curr.value, 1)
                    else:
                        v, c = data[size]
                        v += curr.value
                        c += 1
                        data[level] = (v, c)

                    if curr.left:
                        queue.append(curr.left)
                    if curr.right:
                        queue.append(curr.right)
            return data

        result, data = [], {}
        data = bfs(root)
        i = 1
        while i in data:
            val, count = data[i]
            result.append(int(val / count))
            i += 1
        return result


class PracticeBreadthFirstSearch(object):
    @staticmethod
    def level_order_bfs(root: Node):
        raise NotImplementedError

    @staticmethod
    def get_avg_for_each_level(root: Node) -> list[int]:
        """
        Given the root node of a binary tree, return a list containing the average of each level.
        :param root: Root node of binary tree
        :return: List of averages for each level
        """
        raise NotImplementedError
