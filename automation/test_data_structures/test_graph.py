from __future__ import annotations

import numpy as np
import pytest
from automation.resources.data_structures.graph_data import (
    GRAPH_ADJACENCY_LIST_OUTPUT,
    GRAPH_ADJACENCY_MATRIX_OUTPUT,
    GRAPH_UNION_FIND_FIND_TESTS,
    GRAPH_UNION_FIND_IS_CONNECTED_TESTS,
    GRAPH_UNION_FIND_UNION_TESTS,
    GRAPH_PROBLEM_NUMBER_OF_ISLANDS_2_TESTS,
)
from cs_fundamentals.data_structures.graph import (
    UndirectedGraphVertex,
    UndirectedGraph,
    UnionFind,
    GraphProblems,
)


class TestGraph:
    """
    Canonical/positive-path tests that match the resource fixtures, plus
    a set of edge-case tests that exercise early returns and type checks.
    """

    @classmethod
    def setup_class(cls) -> None:
        cls.search = UnionFind(10)
        cls.undirected_graph = UndirectedGraph()
        cls.problems = GraphProblems()
        cls.node_a = UndirectedGraphVertex("A")
        cls.node_b = UndirectedGraphVertex("B")
        cls.node_c = UndirectedGraphVertex("C")
        cls.node_d = UndirectedGraphVertex("D")
        cls.node_e = UndirectedGraphVertex("E")

    # ---------- Base positive-path tests ----------

    def test_build_undirected_graph_vertices(self) -> None:
        assert self.node_a is not None
        assert self.node_b is not None
        assert self.node_c is not None
        assert self.node_d is not None
        assert self.node_e is not None

    def test_undirected_graph_add_neighbors(self) -> None:
        result = self.node_a.add_neighbors([self.node_b, self.node_c, self.node_e])
        result &= self.node_b.add_neighbors([self.node_a, self.node_c])
        result &= self.node_c.add_neighbors([self.node_b, self.node_d, self.node_a, self.node_e])
        result &= self.node_d.add_neighbor(self.node_c)
        result &= self.node_e.add_neighbors([self.node_a, self.node_c])
        assert result is True

    def test_undirected_graph_add_vertices(self) -> None:
        result = self.undirected_graph.add_vertices(
            [self.node_a, self.node_b, self.node_c, self.node_d, self.node_e]
        )
        assert result is True

    def test_undirected_graph_add_edge(self) -> None:
        result = self.undirected_graph.add_edge(self.node_b, self.node_d)
        assert result is True

    def test_undirected_graph_get_adjacency_list(self) -> None:
        result = self.undirected_graph.get_adjacency_list()
        assert result == GRAPH_ADJACENCY_LIST_OUTPUT

    def test_undirected_graph_get_adjacency_matrix(self) -> None:
        result = self.undirected_graph.get_adjacency_matrix()
        assert str(result) == GRAPH_ADJACENCY_MATRIX_OUTPUT

    @pytest.mark.parametrize("x, y", GRAPH_UNION_FIND_UNION_TESTS)
    def test_union_find_union(self, x, y) -> None:
        # 1-2-5-6-7 3-8-9 4
        result = self.search.union(x, y)
        assert result is True

    @pytest.mark.parametrize("value, output", GRAPH_UNION_FIND_FIND_TESTS)
    def test_union_find_find(self, value, output) -> None:
        result = self.search.find(value)
        assert result == output

    @pytest.mark.parametrize("x, y, output", GRAPH_UNION_FIND_IS_CONNECTED_TESTS)
    def test_union_find_is_connected(self, x, y, output) -> None:
        result = self.search.is_connected(x, y)
        assert result is output

    @pytest.mark.parametrize("m, n, positions, output", GRAPH_PROBLEM_NUMBER_OF_ISLANDS_2_TESTS)
    def test_problem_number_of_islands_2(self, m, n, positions, output) -> None:
        result = self.problems.number_of_islands_2(m, n, positions)
        assert result == output

    # ---------- Additional edge-case tests merged from “extra” ----------

    def test_vertex_add_neighbor_invalid_type_returns_false_no_change(self) -> None:
        v = UndirectedGraphVertex("X")
        before = list(v.neighbors)
        assert v.add_neighbor("not-a-vertex") is False
        assert v.neighbors == before  # Unchanged

        # add_neighbors aggregates results (bitwise-AND), so a bad entry yields False
        v2 = UndirectedGraphVertex("Y")
        assert v.add_neighbors([v2, "oops"]) is False
        assert v.neighbors == ["Y"]  # Only valid neighbor added, sorted

    def test_graph_add_vertex_invalid_type_returns_false(self) -> None:
        g = UndirectedGraph()
        assert g.add_vertex("not-a-vertex") is False  # type: ignore[arg-type]
        assert g.vertices == {}

    def test_graph_add_edge_invalid_types_returns_false(self) -> None:
        g = UndirectedGraph()
        a = UndirectedGraphVertex("A")
        # One bad, one good
        assert g.add_edge(a, "bad") is False  # type: ignore[arg-type]
        # Both bad
        assert g.add_edge("bad", "worse") is False  # type: ignore[arg-type,call-arg]
        # Still empty graph
        assert g.vertices == {}

    def test_graph_add_edges_with_invalid_entry_returns_false(self) -> None:
        g = UndirectedGraph()
        a = UndirectedGraphVertex("A")
        b = UndirectedGraphVertex("B")
        # Include a bad edge tuple; aggregate result becomes False
        assert g.add_edges([(a, b), (a, "nope")]) is False  # type: ignore[list-item]
        # Only the valid edge should have registered in vertices mapping
        assert "A" in g.vertices or "B" in g.vertices

    def test_empty_graph_adjacency_list_and_matrix_are_empty(self) -> None:
        g = UndirectedGraph()
        # build_* should gracefully return empty structures when no vertices
        adj_list = g.get_adjacency_list()
        assert adj_list == []
        adj_matrix = g.get_adjacency_matrix()
        # Code returns [] when empty; normalize to ndarray for assertion
        if isinstance(adj_matrix, list):
            assert adj_matrix == []
        else:
            assert isinstance(adj_matrix, np.ndarray)
            assert adj_matrix.size == 0

    def test_empty_graph_repr_contains_empty_structures(self) -> None:
        g = UndirectedGraph()
        s = repr(g)
        # Should look like "[]\n\n[]"
        assert "[]" in s
        assert s.strip().startswith("[") and s.strip().endswith("]")

    def test_remove_duplicates_staticmethod_dedupes_positions(self) -> None:
        """
        The staticmethod is defined with a stray 'self' parameter; call with None.
        Ensure duplicates/order collapse to unique rows.
        """
        positions = [[1, 2], [1, 2], [2, 3], [2, 3], [3, 4]]
        deduped = GraphProblems.UnionFind.remove_duplicates(None, positions)
        # Order after dict.fromkeys over tuples == insertion order of the first occurrence
        assert deduped == [[1, 2], [2, 3], [3, 4]]
