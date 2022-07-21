"""
Automation Data Structure Graph Test Data
"""

GRAPH_ADJACENCY_LIST_OUTPUT = ["A:['B', 'C', 'E']", "B:['A', 'C', 'D']", "C:['A', 'B', 'D', 'E']", "D:['B', 'C']", "E:['A', 'C']"]
GRAPH_ADJACENCY_MATRIX_OUTPUT = "[[0. 1. 1. 0. 1.]\n" \
                                " [1. 0. 1. 1. 0.]\n" \
                                " [1. 1. 0. 1. 1.]\n" \
                                " [0. 1. 1. 0. 0.]\n" \
                                " [1. 0. 1. 0. 0.]]"
GRAPH_UNION_FIND_FIND_TESTS = [(1, 1), (2, 1), (3, 3), (4, 4), (5, 1), (6, 1), (7, 1), (8, 3), (9, 3)]
GRAPH_UNION_FIND_IS_CONNECTED_TESTS = [
    (1, 5, True),
    (5, 7, True),
    (2, 6, True),
    (3, 8, True),
    (8, 9, True),
    (4, 9, False)]
GRAPH_UNION_FIND_UNION_TESTS = [(1, 2), (2, 5), (5, 6), (6, 7), (3, 8), (8, 9)]  # 1-2-5-6-7 3-8-9 4
GRAPH_PROBLEM_NUMBER_OF_ISLANDS_2_TESTS = [
    (3, 3, [[0, 0], [0, 1], [1, 2], [2, 1]], [1, 1, 2, 3]),
    (3, 3, [[0, 1], [1, 2], [2, 1], [1, 0], [0, 2], [0, 0], [1, 1]], [1, 2, 3, 4, 3, 2, 1]),
    (3, 3, [[0, 0], [0, 1], [1, 2], [1, 2]], [1, 1, 2, 2])]
