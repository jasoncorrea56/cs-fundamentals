from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TestTarget:
    """
    Configuration for a practice target (module + class_name(s) + tests)
    """

    key: str  # Unique id, i.e. "patterns.bfs"
    module: str  # Import path to module under cs_fundamentals
    class_name: str | list[str]  # Target Practice* class(es)
    test_files: list[str]  # Automation tests to run
    test_expr: str  # pytest -k expression
    kind: str  # "pattern" | "data-structure"


# Runner Config Registry
#   To add a new endpoint:
#     - Create an entry in this MATRIX
#     - Create a new runner under router/ using the new entry key to pull handler from factory
#     - Wire up route in main.py
MATRIX: dict[str, TestTarget] = {
    # Data Structures
    "ds.bst": TestTarget(
        key="ds.bst",
        module="cs_fundamentals.data_structures.binary_search_tree",
        class_name="PracticeBinarySearchTree",
        test_files=[
            "automation/test_data_structures/test_binary_search_tree.py",
            "automation/test_data_structures/test_practice/test_practice_binary_search_tree.py",
        ],
        test_expr="BinarySearchTree or PracticeBinarySearchTree",
        kind="data-structure",
    ),
    "ds.graph.islands": TestTarget(
        key="ds.graph.islands",
        module="cs_fundamentals.data_structures.graph",
        class_name="PracticeGraphProblems",
        test_files=[
            "automation/test_data_structures/test_graph.py",
            "automation/test_data_structures/test_practice/test_practice_graph.py",
        ],
        test_expr="number_of_islands_2",
        kind="data-structure",
    ),
    "ds.graph.union_find": TestTarget(
        key="ds.graph.union_find",
        module="cs_fundamentals.data_structures.graph",
        class_name="PracticeUnionFind",
        test_files=[
            "automation/test_data_structures/test_graph.py",
            "automation/test_data_structures/test_practice/test_practice_graph.py",
        ],
        test_expr="not number_of_islands_2",
        kind="data-structure",
    ),
    "ds.linked_list_double": TestTarget(
        key="ds.linked_list_double",
        module="cs_fundamentals.data_structures.linked_list_double",
        class_name="PracticeDoublyLinkedList",
        test_files=[
            "automation/test_data_structures/test_linked_list_double.py",
            "automation/test_data_structures/test_practice/test_practice_linked_list_double.py",
        ],
        test_expr="linked_list_double",
        kind="data-structure",
    ),
    "ds.linked_list_single": TestTarget(
        key="ds.linked_list_single",
        module="cs_fundamentals.data_structures.linked_list_single",
        class_name="PracticeSinglyLinkedList",
        test_files=[
            "automation/test_data_structures/test_linked_list_single.py",
            "automation/test_data_structures/test_practice/test_practice_linked_list_single.py",
        ],
        test_expr="linked_list_single",
        kind="data-structure",
    ),
    "ds.max_heap": TestTarget(
        key="ds.max_heap",
        module="cs_fundamentals.data_structures.max_heap",
        class_name="PracticeMaxHeap",
        test_files=[
            "automation/test_data_structures/test_max_heap.py",
            "automation/test_data_structures/test_practice/test_practice_max_heap.py",
        ],
        test_expr="MaxHeap or PracticeMaxHeap",
        kind="data-structure",
    ),
    "ds.min_heap": TestTarget(
        key="ds.min_heap",
        module="cs_fundamentals.data_structures.min_heap",
        class_name="PracticeMinHeap",
        test_files=[
            "automation/test_data_structures/test_min_heap.py",
            "automation/test_data_structures/test_practice/test_practice_min_heap.py",
        ],
        test_expr="MinHeap or PracticeMinHeap",
        kind="data-structure",
    ),
    "ds.queue.array": TestTarget(
        key="ds.queue.array",
        module="cs_fundamentals.data_structures.queue",
        class_name="PracticeQueueCircularArray",
        test_files=[
            "automation/test_data_structures/test_queue.py",
            "automation/test_data_structures/test_practice/test_practice_queue.py",
        ],
        test_expr="array",
        kind="data-structure",
    ),
    "ds.queue.linked_list": TestTarget(
        key="ds.queue.linked_list",
        module="cs_fundamentals.data_structures.queue",
        class_name="PracticeQueueCircularLinkedList",
        test_files=[
            "automation/test_data_structures/test_queue.py",
            "automation/test_data_structures/test_practice/test_practice_queue.py",
        ],
        test_expr="linked_list",
        kind="data-structure",
    ),
    "ds.stack.array": TestTarget(
        key="ds.stack.array",
        kind="data-structure",
        module="cs_fundamentals.data_structures.stack",
        class_name="PracticeStackArray",
        test_files=[
            "automation/test_data_structures/test_stack.py",
            "automation/test_data_structures/test_practice/test_practice_stack.py",
        ],
        test_expr="array",
    ),
    "ds.stack.linked_list": TestTarget(
        key="ds.stack.linked_list",
        kind="data-structure",
        module="cs_fundamentals.data_structures.stack",
        class_name="PracticeStackLinkedList",
        test_files=[
            "automation/test_data_structures/test_stack.py",
            "automation/test_data_structures/test_practice/test_practice_stack.py",
        ],
        test_expr="linked_list",
    ),
    # Patterns
    "patterns.bfs": TestTarget(
        key="patterns.bfs",
        module="cs_fundamentals.patterns.breadth_first_search",
        class_name="PracticeBreadthFirstSearch",
        test_files=[
            "automation/test_patterns/test_breadth_first_search.py",
            "automation/test_patterns/test_practice/test_practice_breadth_first_search.py",
        ],
        test_expr="breadth_first_search or PracticeBreadthFirstSearch",
        kind="pattern",
    ),
    "patterns.dfs": TestTarget(
        key="patterns.dfs",
        module="cs_fundamentals.patterns.depth_first_search",
        class_name="PracticeDepthFirstSearch",
        test_files=[
            "automation/test_patterns/test_depth_first_search.py",
            "automation/test_patterns/test_practice/test_practice_depth_first_search.py",
        ],
        test_expr="depth_first_search or PracticeDepthFirstSearch",
        kind="pattern",
    ),
    "patterns.fast_slow_pointers": TestTarget(
        key="patterns.fast_slow_pointers",
        module="cs_fundamentals.patterns.fast_slow_pointers",
        class_name="PracticeFastSlowPointers",
        test_files=[
            "automation/test_patterns/test_fast_slow_pointers.py",
            "automation/test_patterns/test_practice/test_practice_fast_slow_pointers.py",
        ],
        test_expr="fast_slow_pointers or PracticeFastSlowPointers",
        kind="pattern",
    ),
    "patterns.singleton": TestTarget(
        key="patterns.singleton",
        module="cs_fundamentals.patterns.singleton",
        class_name="PracticeSingletonClass",
        test_files=[
            "automation/test_patterns/test_singleton.py",
            "automation/test_patterns/test_practice/test_practice_singleton.py",
        ],
        test_expr="singleton",
        kind="pattern",
    ),
    "patterns.sorting": TestTarget(
        key="patterns.sorting",
        module="cs_fundamentals.patterns.sorting",
        class_name="PracticeSortingAlgorithms",
        test_files=[
            "automation/test_patterns/test_sorting.py",
            "automation/test_patterns/test_practice/test_practice_sorting.py",
        ],
        test_expr="SortingAlgorithms or PracticeSortingAlgorithms",
        kind="pattern",
    ),
    "patterns.sliding_window": TestTarget(
        key="patterns.sliding_window",
        module="cs_fundamentals.patterns.sliding_window",
        class_name="PracticeSlidingWindow",
        test_files=[
            "automation/test_patterns/test_sliding_window.py",
            "automation/test_patterns/test_practice/test_practice_sliding_window.py",
        ],
        test_expr="sliding_window or PracticeSlidingWindow",
        kind="pattern",
    ),
    "patterns.two_pointers": TestTarget(
        key="patterns.two_pointers",
        module="cs_fundamentals.patterns.two_pointers",
        class_name="PracticeTwoPointers",
        test_files=[
            "automation/test_patterns/test_two_pointers.py",
            "automation/test_patterns/test_practice/test_practice_two_pointers.py",
        ],
        test_expr="two_pointers or PracticeTwoPointers",
        kind="pattern",
    ),
}


def get_target(key: str) -> TestTarget:
    try:
        return MATRIX[key]
    except KeyError as exc:  # noqa: PERF203
        raise KeyError(f"Unknown target '{key}'. Use one of: {', '.join(sorted(MATRIX))}") from exc


def list_targets(kind: str | None = None) -> list[TestTarget]:
    items: list[TestTarget] = list(MATRIX.values())
    if kind:
        items = [t for t in items if t.kind == kind]
    return sorted(items, key=lambda t: t.key)
