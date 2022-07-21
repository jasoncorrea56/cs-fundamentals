

class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class DepthFirstSearch(object):

    def preorder_dfs(self, node, data):
        if not node:
            return None

        data.append(node.value)
        self.preorder_dfs(node.left, data)
        self.preorder_dfs(node.right, data)
        return

    def inorder_dfs(self, node, data):
        if not node:
            return None

        self.inorder_dfs(node.left, data)
        data.append(node.value)
        self.inorder_dfs(node.right, data)
        return

    def postorder_dfs(self, node, data):
        if not node:
            return None

        self.postorder_dfs(node.left, data)
        self.postorder_dfs(node.right, data)
        data.append(node.value)
        return

    @staticmethod
    def get_avg_for_each_level(root: Node) -> list[int]:
        """
        Given the root node of a binary tree, return a list containing the average of each level.
        :param root: Root node of binary tree
        :return: List of averages for each level
        """
        def preorder_dfs(node, level=0):
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

        data = {}
        preorder_dfs(root)
        result = []
        i = 0
        while i in data:
            val, count = data[i]
            result.append(val / count)
            i += 1
        return result


class PracticeDepthFirstSearch(object):

    def preorder_dfs(self, node, data):
        raise NotImplementedError

    def inorder_dfs(self, node, data):
        raise NotImplementedError

    def postorder_dfs(self, node, data):
        raise NotImplementedError

    def get_avg_for_each_level(self, root: Node) -> list[int]:
        """
        Given the root node of a binary tree, return a list containing the average of each level.
        :param root: Root node of binary tree
        :return: List of averages for each level
        """
        raise NotImplementedError
