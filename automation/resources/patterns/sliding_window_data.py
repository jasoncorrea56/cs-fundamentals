"""
Automation Pattern Sliding Window Test Data
"""

from typing import Any


SLIDING_WINDOW_AVG_OUTPUT: list[float] = [2.2, 2.8, 2.4, 3.6, 2.8]
SLIDING_WINDOW_AVG_NUMS: list[int] = [1, 3, 2, 6, -1, 4, 1, 8, 2]
SLIDING_WINDOW_AVG_K: int = 5
SLIDING_WINDOW_MAX_SUBARRAY_OF_SIZE_K_TESTS: list[Any] = [
    ([2, 1, 5, 1, 3, 2], 3, 9),
    ([2, 1, 5, 0, 7, 2, 4, 8, 6], 3, 18),
    ([2, 3, 4, 1, 5], 2, 7),
]
SLIDING_WINDOW_SMALLEST_SUBARRAY_SUM_GREATER_THAN_S_TESTS: list[Any] = [
    ([2, 1, 5, 2, 3, 2], 7, 2),
    ([2, 1, 5, 2, 8], 7, 1),
    ([3, 4, 1, 1, 6], 8, 3),
]
SLIDING_WINDOW_LONGEST_SUBSTRING_WITH_K_DISTINCT_CHARS_TESTS: list[Any] = [
    ("araaci", 2, 4),
    ("araaci", 1, 2),
    ("cbbebi", 3, 5),
]
SLIDING_WINDOW_FRUITS_INTO_BASKETS_TESTS: list[Any] = [
    (["A", "B", "C", "A", "C"], 3),
    (["A", "B", "C", "B", "B", "C"], 5),
]
SLIDING_WINDOW_LONGEST_SUBSTRING_WITH_DISTINCT_CHARS_TESTS: list[Any] = [
    ("aabccbb", 3),
    ("abbbb", 2),
    ("abba", 2),
    ("abccde", 3),
]
SLIDING_WINDOW_LONGEST_SUBSTRING_WITH_SAME_LETTERS_AFTER_REPLACEMENT_TESTS: list[
    Any
] = [
    ("aabccbb", 2, 5),
    ("abbcb", 1, 4),
    ("abccde", 1, 3),
]
SLIDING_WINDOW_LONGEST_SUBARRAY_WITH_ONES_AFTER_REPLACEMENT_TESTS: list[Any] = [
    ([0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1], 2, 6),
    ([0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1], 3, 9),
]
