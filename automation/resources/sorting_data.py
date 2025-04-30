"""
Automation Sorting Test Data
"""

from typing import Any


SORT_AVG_EXPECTED_OUTPUT: list[float] = [2.2, 2.8, 2.4, 3.6, 2.8]
SORT_MAX_EXPECTED_OUTPUT: int = 0
SORT_X: int = 4
SORT_Y: int = 6
SORT_BUCKET_NUMS: list[float] = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
SORT_SORTED_BUCKET_NUMS_OUTPUT: list[float] = [
    0.1234,
    0.3434,
    0.565,
    0.656,
    0.665,
    0.897,
]
SORT_SELECTION_TESTS: list[Any] = [
    ([1, 3, 2, 6, 9, 7, 4, 8, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9])
]
SORT_BUBBLE_TESTS: list[Any] = [
    ([1, 3, 2, 6, 9, 7, 4, 8, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9])
]
SORT_INSERTION_TESTS: list[Any] = [
    ([1, 3, 2, 6, 9, 7, 4, 8, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9])
]
SORT_MERGE_TESTS: list[Any] = [
    ([1, 3, 2, 6, 9, 7, 4, 8, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9])
]
SORT_QUICK_TESTS: list[Any] = [
    ([1, 3, 2, 6, 9, 7, 4, 8, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9])
]
SORT_HEAP_TESTS: list[Any] = [
    ([1, 3, 2, 6, 9, 7, 4, 8, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9])
]
SORT_RADIX_TESTS: list[Any] = [
    ([1, 3, 2, 6, 9, 7, 4, 8, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9])
]
SORT_STALIN_TESTS: list[Any] = [([1, 3, 2, 6, 9, 7, 4, 8, 5], [1, 3, 6, 9])]
