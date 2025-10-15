import pytest
from automation.resources.data_structures.graph_data import (
    GRAPH_UNION_FIND_FIND_TESTS,
    GRAPH_UNION_FIND_IS_CONNECTED_TESTS,
    GRAPH_UNION_FIND_UNION_TESTS,
    GRAPH_PROBLEM_NUMBER_OF_ISLANDS_2_TESTS,
)
from automation.test_data_structures.test_graph import TestGraph
from cs_fundamentals.data_structures.graph import (
    UndirectedGraphVertex,
    UndirectedGraph,
    PracticeUnionFind,
    PracticeGraphProblems,
)


class TestPracticeGraph(TestGraph):
    @classmethod
    def setup_class(cls) -> None:
        cls.search = PracticeUnionFind(10)
        cls.undirected_graph = UndirectedGraph()
        cls.problems = PracticeGraphProblems()
        cls.node_a = UndirectedGraphVertex("A")
        cls.node_b = UndirectedGraphVertex("B")
        cls.node_c = UndirectedGraphVertex("C")
        cls.node_d = UndirectedGraphVertex("D")
        cls.node_e = UndirectedGraphVertex("E")

    def test_build_undirected_graph_vertices(self) -> None:
        try:
            super().test_build_undirected_graph_vertices()
        except NotImplementedError:
            assert True

    def test_undirected_graph_add_neighbors(self) -> None:
        try:
            super().test_undirected_graph_add_neighbors()
        except NotImplementedError:
            assert True

    def test_undirected_graph_add_vertices(self) -> None:
        try:
            super().test_undirected_graph_add_vertices()
        except NotImplementedError:
            assert True

    def test_undirected_graph_add_edge(self) -> None:
        try:
            super().test_undirected_graph_add_edge()
        except NotImplementedError:
            assert True

    def test_undirected_graph_get_adjacency_list(self) -> None:
        try:
            super().test_undirected_graph_get_adjacency_list()
        except NotImplementedError:
            assert True

    def test_undirected_graph_get_adjacency_matrix(self) -> None:
        try:
            super().test_undirected_graph_get_adjacency_matrix()
        except NotImplementedError:
            assert True

    # def test_undirected_graph_repr(self) -> None:
    #     print("\nUndirected Graph:")
    #     print(self.undirected_graph)
    #     assert True

    @pytest.mark.parametrize("x, y", GRAPH_UNION_FIND_UNION_TESTS)
    def test_union_find_union(self, x, y) -> None:
        try:
            super().test_union_find_union(x, y)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize("value, output", GRAPH_UNION_FIND_FIND_TESTS)
    def test_union_find_find(self, value, output) -> None:
        try:
            super().test_union_find_find(value, output)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize("x, y, output", GRAPH_UNION_FIND_IS_CONNECTED_TESTS)
    def test_union_find_is_connected(self, x, y, output) -> None:
        try:
            super().test_union_find_is_connected(x, y, output)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize(
        "m, n, positions, output", GRAPH_PROBLEM_NUMBER_OF_ISLANDS_2_TESTS
    )
    def test_problem_number_of_islands_2(self, m, n, positions, output) -> None:
        try:
            super().test_problem_number_of_islands_2(m, n, positions, output)
        except NotImplementedError:
            assert True
