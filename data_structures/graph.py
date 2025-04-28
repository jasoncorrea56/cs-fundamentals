import numpy as np


class UndirectedGraphVertex:
    def __init__(self, value):
        self.value = value
        self.neighbors = []

    def add_neighbor(self, neighbor, sort_self=True):
        if isinstance(neighbor, UndirectedGraphVertex):
            if neighbor.value not in self.neighbors:
                # Add neighbor
                self.neighbors.append(neighbor.value)
                neighbor.neighbors.append(self.value)

                # Sort neighbors
                if sort_self:
                    self.neighbors = sorted(self.neighbors)
                neighbor.neighbors = sorted(neighbor.neighbors)
            return True
        else:
            return False

    def add_neighbors(self, neighbors):
        result = True
        for neighbor in neighbors:
            result &= self.add_neighbor(neighbor, False)
        self.neighbors = sorted(self.neighbors)
        return result

    def __repr__(self):
        return str(self.neighbors)


class UndirectedGraph:
    def __init__(self):
        self.vertices = {}
        self.vertex_values = []
        self.vertex_indices = {}
        self.adjacency_list = []
        self.adjacency_matrix = []

    def add_vertex(self, vertex: UndirectedGraphVertex):
        if isinstance(vertex, UndirectedGraphVertex):
            self.vertices[vertex.value] = vertex.neighbors
            return True
        else:
            return False

    def add_vertices(self, vertices: list[UndirectedGraphVertex]):
        result = True
        for vertex in vertices:
            result &= self.add_vertex(vertex)
        return result

    def add_edge(
        self, vertex_from: UndirectedGraphVertex, vertex_to: UndirectedGraphVertex
    ):
        if isinstance(vertex_from, UndirectedGraphVertex) and isinstance(
            vertex_to, UndirectedGraphVertex
        ):
            vertex_from.add_neighbor(vertex_to)
            self.vertices[vertex_from.value] = vertex_from.neighbors
            self.vertices[vertex_to.value] = vertex_to.neighbors
            return True
        else:
            return False

    def add_edges(self, edges):
        result = True
        for edge in edges:
            result &= self.add_edge(edge[0], edge[1])
        return result

    def build_adjacency_list(self):
        if len(self.vertices) >= 1:
            self.adjacency_list = [
                str(key) + ":" + str(self.vertices[key]) for key in self.vertices.keys()
            ]
        return self.adjacency_list

    def build_adjacency_matrix(self):
        if len(self.vertices) >= 1:
            vertex_count = len(self.vertices)
            self.vertex_values = sorted(self.vertices.keys())
            self.vertex_indices = dict(zip(self.vertex_values, range(vertex_count)))
            self.adjacency_matrix = np.zeros(shape=(vertex_count, vertex_count))
            for i in range(vertex_count):
                for j in range(i, vertex_count):
                    for k in self.vertices[self.vertex_values[i]]:
                        j = self.vertex_indices[k]
                        self.adjacency_matrix[i, j] = 1
        return self.adjacency_matrix

    def get_adjacency_list(self):
        """Returns a graph as adjacency list and adjacency matrix."""
        return self.build_adjacency_list()

    def get_adjacency_matrix(self):
        """Function to print a graph as adjacency list and adjacency matrix."""
        return self.build_adjacency_matrix()

    def __repr__(self):
        """Function to print a graph as adjacency list and adjacency matrix."""
        return (
            str(self.build_adjacency_list())
            + "\n\n"
            + str(self.build_adjacency_matrix())
        )


class UnionFind(object):
    """
    UnionFind class - Union by Rank and Path Compression Implementation
    """

    def __init__(self, size):
        self.root = [i for i in range(size)]
        self.rank = [1] * size

    def find(self, x):
        """
        Searches for the root of x
        :param x: Node on which to find the root
        :return: Root node
        """
        if x == self.root[x]:
            return x
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x, y):
        """
        The union function with union by rank, joins to nodes x and y
        :param x: Node to join with y
        :param y: Node to join with x
        :return: True if successful
        """
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.rank[root_x] > self.rank[root_y]:
                self.root[root_y] = root_x
            elif self.rank[root_x] < self.rank[root_y]:
                self.root[root_x] = root_y
            else:
                self.root[root_y] = root_x
                self.rank[root_x] += 1
        return True

    def is_connected(self, x, y):
        """
        Tests if two nodes are connected
        :param x: Node to check if connected to node y
        :param y: Node to check if connected to node x
        :return: True if connected, else False
        """
        return self.find(x) == self.find(y)


class GraphProblems(object):
    class UnionFind(object):
        def __init__(self, size):
            self.root = [-1] * size
            self.rank = [0] * size
            self.count = 0

        def find(self, node):
            if node != self.root[node]:
                self.root[node] = self.find(self.root[node])
            return self.root[node]

        def union(self, node_x, node_y):
            root_x = self.find(node_x)
            root_y = self.find(node_y)
            if root_x != root_y:
                if self.rank[root_x] > self.rank[root_y]:
                    self.root[root_y] = root_x
                elif self.rank[root_x] < self.rank[root_y]:
                    self.root[root_x] = root_y
                else:
                    self.root[root_y] = root_x
                    self.rank[root_x] += 1
                self.count -= 1
            return

        def is_valid(self, node):
            return self.root[node] >= 0

        def set_parent(self, node):
            self.root[node] = node
            self.count += 1
            return

        @staticmethod
        def remove_duplicates(self, positions):
            seen = set()
            clean = dict.fromkeys(tuple(tuple(x) for x in positions))
            result = [list(x) for x in clean if not (x in seen or seen.add(x))]
            return result

    def number_of_islands_2(
        self, m: int, n: int, positions: list[list[int]]
    ) -> list[int]:
        """
        Given an empty 2D binary grid of size m x n, where the grid represents a map.
          - 0's represent water
          - 1's represent land
        Initially, all the cells of grid are water cells (0's).

        Performing an add land operation turns the water at the given position into land.
        You are given array positions where positions[i] = [ri, ci] is the position (ri, ci)
        at which a land operation is performed.

        Return an array of integers where answer[i] is the number of islands after turning cell (ri, ci) into land.

        An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically only.
        Assume all four edges of the grid are all surrounded by water.
        :param m: Number of rows in the grid
        :param n: Number of columns in the grid
        :param positions: List of x and y grid coordinates indicating land
        :return: An array of integers where answer[i] is the number of islands after turning the cell (ri, ci) into land
        """
        result = []
        uf = self.UnionFind(m * n)

        for pos in positions:
            r, c = pos[0], pos[1]
            overlap = []

            index = (r - 1) * n + c
            if (r - 1 >= 0) and (uf.is_valid(index)):
                overlap.append(index)

            index = (r + 1) * n + c
            if (r + 1 < m) and (uf.is_valid(index)):
                overlap.append(index)

            index = r * n + (c - 1)
            if (c - 1 >= 0) and (uf.is_valid(index)):
                overlap.append(index)

            index = r * n + (c + 1)
            if (c + 1 < n) and (uf.is_valid(index)):
                overlap.append(index)

            index = r * n + c
            if not uf.is_valid(index):
                uf.set_parent(index)

            for i in overlap:
                uf.union(i, index)

            result.append(uf.count)
        return result


class PracticeUnionFind(object):
    """
    UnionFind class - Union by Rank and Path Compression Implementation
    """

    def __init__(self, size):
        pass

    def find(self, x):
        """
        Searches for the root of x
        :param x: Node on which to find the root
        :return: Root node
        """
        raise NotImplementedError

    def union(self, x, y):
        """
        The union function with union by rank, joins to nodes x and y
        Unimplemented Stub:
        return True
        :param x: Node to join with y
        :param y: Node to join with x
        :return: True if successful
        """
        raise NotImplementedError

    def is_connected(self, x, y):
        """
        Tests if two nodes are connected
        :param x: Node to check if connected to node y
        :param y: Node to check if connected to node x
        :return: True if connected, else False
        """
        raise NotImplementedError


class PracticeGraphProblems(object):
    class UnionFind(object):
        def __init__(self, size):
            pass

        def find(self, node):
            raise NotImplementedError

        def union(self, node_x, node_y):
            raise NotImplementedError

        def is_valid(self, node):
            raise NotImplementedError

        def set_parent(self, node):
            raise NotImplementedError

    def number_of_islands_2(
        self, m: int, n: int, positions: list[list[int]]
    ) -> list[int]:
        """
        Given an empty 2D binary grid of size m x n, where the grid represents a map.
          - 0's represent water
          - 1's represent land
        Initially, all the cells of grid are water cells (0's).

        Performing an add land operation turns the water at the given position into land.
        You are given array positions where positions[i] = [ri, ci] is the position (ri, ci)
        at which a land operation is performed.

        Return an array of integers where answer[i] is the number of islands after turning cell (ri, ci) into land.

        An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically only.
        Assume all four edges of the grid are all surrounded by water.
        :param m: Number of rows in the grid
        :param n: Number of columns in the grid
        :param positions: List of x and y grid coordinates indicating land
        :return: An array of integers where answer[i] is the number of islands after turning the cell (ri, ci) into land
        """
        raise NotImplementedError
