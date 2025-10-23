from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray
    from collections.abc import Hashable


class UndirectedGraphVertex:
    def __init__(self, value: Hashable) -> None:
        self.value: Hashable = value
        self.neighbors: list[Hashable] = []

    def add_neighbor(self, neighbor: UndirectedGraphVertex, sort_self: bool = True) -> bool:
        if not isinstance(neighbor, UndirectedGraphVertex):
            return False

        if neighbor.value not in self.neighbors:
            # Add neighbor
            self.neighbors.append(neighbor.value)
            neighbor.neighbors.append(self.value)

            # Sort neighbors
            if sort_self:
                self.neighbors = sorted(self.neighbors, key=lambda x: str(x))
            neighbor.neighbors = sorted(neighbor.neighbors, key=lambda x: str(x))
        return True

    def add_neighbors(self, neighbors: list[UndirectedGraphVertex]) -> bool:
        result: bool = True
        for neighbor in neighbors:
            result &= self.add_neighbor(neighbor, sort_self=False)
        # Final sort after bulk additions
        self.neighbors = sorted(self.neighbors, key=lambda x: str(x))
        return result

    def __repr__(self) -> str:
        return str(self.neighbors)


class UndirectedGraph:
    def __init__(self) -> None:
        # Map vertex value -> list of neighbor values
        self.vertices: dict[Hashable, list[Hashable]] = {}
        self.vertex_values: list[Hashable] = []
        self.vertex_indices: dict[Hashable, int] = {}
        self.adjacency_list: list[str] = []
        self.adjacency_matrix: NDArray[np.float64] = np.zeros((0, 0), dtype=np.float64)

    def add_vertex(self, vertex: UndirectedGraphVertex) -> bool:
        if not isinstance(vertex, UndirectedGraphVertex):
            return False
        self.vertices[vertex.value] = vertex.neighbors
        return True

    def add_vertices(self, vertices: list[UndirectedGraphVertex]) -> bool:
        result = True
        for vertex in vertices:
            result &= self.add_vertex(vertex)
        return result

    def add_edge(
        self, vertex_from: UndirectedGraphVertex, vertex_to: UndirectedGraphVertex
    ) -> bool:
        if not (
            isinstance(vertex_from, UndirectedGraphVertex)
            and isinstance(vertex_to, UndirectedGraphVertex)
        ):
            return False
        vertex_from.add_neighbor(vertex_to)
        self.vertices[vertex_from.value] = vertex_from.neighbors
        self.vertices[vertex_to.value] = vertex_to.neighbors
        return True

    def add_edges(self, edges: list[tuple[UndirectedGraphVertex, UndirectedGraphVertex]]) -> bool:
        result = True
        for v_from, v_to in edges:
            result &= self.add_edge(v_from, v_to)
        return result

    def build_adjacency_list(self) -> list[str]:
        if self.vertices:
            self.adjacency_list = [f"{key}:{self.vertices[key]}" for key in self.vertices]
        else:
            self.adjacency_list = []
        return self.adjacency_list

    def build_adjacency_matrix(self) -> NDArray[np.float64]:
        if self.vertices:
            vertex_count = len(self.vertices)
            self.vertex_values = sorted(self.vertices.keys(), key=lambda x: str(x))
            self.vertex_indices = {val: i for i, val in enumerate(self.vertex_values)}
            mat = np.zeros((vertex_count, vertex_count), dtype=np.float64)

            for i in range(vertex_count):
                # neighbors are stored as values; translate to indices
                for neighbor_val in self.vertices[self.vertex_values[i]]:
                    j = self.vertex_indices[neighbor_val]
                    mat[i, j] = 1.0

            self.adjacency_matrix = mat
        else:
            self.adjacency_matrix = np.zeros((0, 0), dtype=np.float64)
        return self.adjacency_matrix

    def get_adjacency_list(self) -> list[str]:
        """Returns a graph as adjacency list."""
        return self.build_adjacency_list()

    def get_adjacency_matrix(self) -> NDArray[np.float64]:
        """Returns a graph as adjacency matrix."""
        return self.build_adjacency_matrix()

    def __repr__(self) -> str:
        """Function to print a graph as adjacency list and adjacency matrix."""
        return f"{self.build_adjacency_list()}\n\n{self.build_adjacency_matrix()}"


class UnionFind:
    """
    UnionFind class - Union by Rank and Path Compression Implementation
    """

    def __init__(self, size: int) -> None:
        self.root: list[int] = list(range(size))
        self.rank: list[int] = [1] * size

    def find(self, x: int) -> int:
        """
        Searches for the root of x
        :param x: Node on which to find the root
        :return: Root node
        """
        if x == self.root[x]:
            return x
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x: int, y: int) -> bool:
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

    def is_connected(self, x: int, y: int) -> bool:
        """
        Tests if two nodes are connected
        :param x: Node to check if connected to node y
        :param y: Node to check if connected to node x
        :return: True if connected, else False
        """
        return self.find(x) == self.find(y)


class GraphProblems:
    class UnionFind:
        def __init__(self, size: int) -> None:
            self.root: list[int] = [-1] * size
            self.rank: list[int] = [0] * size
            self.count: int = 0

        def find(self, node: int) -> int:
            if node != self.root[node]:
                self.root[node] = self.find(self.root[node])
            return self.root[node]

        def union(self, node_x: int, node_y: int) -> None:
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

        def is_valid(self, node: int) -> bool:
            return self.root[node] >= 0

        def set_parent(self, node: int) -> None:
            self.root[node] = node
            self.count += 1

        @staticmethod
        def remove_duplicates(positions: list[list[int]]) -> list[list[int]]:
            """
            Remove duplicate positions (treat each position as a 2-item list).
            """
            # Convert to tuples for set semantics, then back to lists
            uniq = {tuple(p) for p in positions}
            return [list(p) for p in uniq]

    def number_of_islands_2(self, m: int, n: int, positions: list[list[int]]) -> list[int]:
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
        result: list[int] = []
        uf = self.UnionFind(m * n)

        for pos in positions:
            r, c = pos[0], pos[1]
            overlap: list[int] = []

            index = (r - 1) * n + c
            if (r - 1 >= 0) and uf.is_valid(index):
                overlap.append(index)

            index = (r + 1) * n + c
            if (r + 1 < m) and uf.is_valid(index):
                overlap.append(index)

            index = r * n + (c - 1)
            if (c - 1 >= 0) and uf.is_valid(index):
                overlap.append(index)

            index = r * n + (c + 1)
            if (c + 1 < n) and uf.is_valid(index):
                overlap.append(index)

            index = r * n + c
            if not uf.is_valid(index):
                uf.set_parent(index)

            for i in overlap:
                uf.union(i, index)

            result.append(uf.count)
        return result


class PracticeUnionFind:
    """
    UnionFind class - Union by Rank and Path Compression Implementation (practice skeleton)
    """

    def __init__(self, size: int) -> None:
        pass

    def find(self, x: int) -> int:
        """
        Searches for the root of x
        :param x: Node for which to find the root
        :return: Root node
        """
        raise NotImplementedError

    def union(self, x: int, y: int) -> bool:
        """
        The union function with union by rank; joins nodes x and y.
        Implementers should return True on success.
        """
        raise NotImplementedError

    def is_connected(self, x: int, y: int) -> bool:
        """
        Tests if two nodes are connected.
        """
        raise NotImplementedError


class PracticeGraphProblems:
    class UnionFind:
        def __init__(self, size: int) -> None:
            pass

        def find(self, node: int) -> int:
            raise NotImplementedError

        def union(self, node_x: int, node_y: int) -> None:
            raise NotImplementedError

        def is_valid(self, node: int) -> bool:
            raise NotImplementedError

        def set_parent(self, node: int) -> None:
            raise NotImplementedError

    def number_of_islands_2(self, m: int, n: int, positions: list[list[int]]) -> list[int]:
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
