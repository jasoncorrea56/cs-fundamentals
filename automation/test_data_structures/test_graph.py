import pytest
from automation.resources.data_structures.graph_data import (
    GRAPH_ADJACENCY_LIST_OUTPUT,
    GRAPH_ADJACENCY_MATRIX_OUTPUT,
    GRAPH_UNION_FIND_FIND_TESTS,
    GRAPH_UNION_FIND_IS_CONNECTED_TESTS,
    GRAPH_UNION_FIND_UNION_TESTS,
    GRAPH_PROBLEM_NUMBER_OF_ISLANDS_2_TESTS,
)
from data_structures.graph import (
    UndirectedGraphVertex,
    UndirectedGraph,
    UnionFind,
    GraphProblems,
)


class TestGraph(object):
    @classmethod
    def setup_class(cls):
        cls.search = UnionFind(10)
        cls.undirected_graph = UndirectedGraph()
        cls.problems = GraphProblems()
        cls.node_a = UndirectedGraphVertex("A")
        cls.node_b = UndirectedGraphVertex("B")
        cls.node_c = UndirectedGraphVertex("C")
        cls.node_d = UndirectedGraphVertex("D")
        cls.node_e = UndirectedGraphVertex("E")

    def test_build_undirected_graph_vertices(self):
        assert self.node_a is not None
        assert self.node_b is not None
        assert self.node_c is not None
        assert self.node_d is not None
        assert self.node_e is not None

    def test_undirected_graph_add_neighbors(self):
        result = self.node_a.add_neighbors([self.node_b, self.node_c, self.node_e])
        result &= self.node_b.add_neighbors([self.node_a, self.node_c])
        result &= self.node_c.add_neighbors(
            [self.node_b, self.node_d, self.node_a, self.node_e]
        )
        result &= self.node_d.add_neighbor(self.node_c)
        result &= self.node_e.add_neighbors([self.node_a, self.node_c])
        assert result is True

    def test_undirected_graph_add_vertices(self):
        result = self.undirected_graph.add_vertices(
            [self.node_a, self.node_b, self.node_c, self.node_d, self.node_e]
        )
        assert result is True

    def test_undirected_graph_add_edge(self):
        result = self.undirected_graph.add_edge(self.node_b, self.node_d)
        assert result is True

    def test_undirected_graph_get_adjacency_list(self):
        result = self.undirected_graph.get_adjacency_list()
        assert result == GRAPH_ADJACENCY_LIST_OUTPUT

    def test_undirected_graph_get_adjacency_matrix(self):
        result = self.undirected_graph.get_adjacency_matrix()
        assert str(result) == GRAPH_ADJACENCY_MATRIX_OUTPUT

    # def test_undirected_graph_repr(self):
    #     print("\nUndirected Graph:")
    #     print(self.undirected_graph)
    #     assert True

    @pytest.mark.parametrize("x, y", GRAPH_UNION_FIND_UNION_TESTS)
    def test_union_find_union(self, x, y):
        # 1-2-5-6-7 3-8-9 4
        result = self.search.union(x, y)
        assert result is True

    @pytest.mark.parametrize("value, output", GRAPH_UNION_FIND_FIND_TESTS)
    def test_union_find_find(self, value, output):
        result = self.search.find(value)
        assert result == output

    @pytest.mark.parametrize("x, y, output", GRAPH_UNION_FIND_IS_CONNECTED_TESTS)
    def test_union_find_is_connected(self, x, y, output):
        result = self.search.is_connected(x, y)
        assert result is output

    @pytest.mark.parametrize(
        "m, n, positions, output", GRAPH_PROBLEM_NUMBER_OF_ISLANDS_2_TESTS
    )
    def test_problem_number_of_islands_2(self, m, n, positions, output):
        result = self.problems.number_of_islands_2(m, n, positions)
        assert result == output
