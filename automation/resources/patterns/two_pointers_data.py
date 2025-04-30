"""
Automation Pattern Two Pointers Test Data
"""

from typing import Any


TWO_POINTERS_TWO_SUM_TESTS: list[Any] = [
    ([1, 2, 3, 4, 6], 6, [1, 3]),
    ([2, 5, 9, 11], 11, [0, 2]),
]
TWO_POINTERS_REMOVE_DUPLICATES_TESTS: list[Any] = [
    ([2, 3, 3, 3, 6, 9, 9], 4),
    ([2, 2, 2, 11], 2),
]
TWO_POINTERS_REMOVE_DUPLICATE_KEY_TESTS: list[Any] = [
    ([3, 2, 3, 6, 3, 10, 9, 3], 3, 4),
    ([2, 11, 2, 2, 1], 2, 2),
]
TWO_POINTERS_SQUARE_SORTED_ARRAY_TESTS: list[Any] = [
    ([-2, -1, 0, 2, 3], [0, 1, 4, 4, 9]),
    ([-3, -1, 0, 1, 2], [0, 1, 1, 4, 9]),
]
TWO_POINTERS_THREE_SUM_TESTS: list[Any] = [
    ([-3, 0, 1, 2, -1, 1, -2], [[-3, 1, 2], [-2, 0, 2], [-2, 1, 1], [-1, 0, 1]]),
    ([-5, 2, -1, -2, 3], [[-5, 2, 3], [-2, -1, 3]]),
]
TWO_POINTERS_THREE_SUM_TO_TARGET_TESTS: list[Any] = [
    ([-2, 0, 1, 2], 2, 1),
    ([-3, -1, 1, 2], 1, 0),
    ([1, 0, 1, 1], 100, 3),
]
TWO_POINTERS_TRIPLETS_WITH_SMALLER_SUM_TESTS: list[Any] = [
    ([-1, 0, 2, 3], 3, 2),
    ([-1, 4, 2, 1, 3], 5, 4),
]
TWO_POINTERS_SUBARRAYS_WITH_PRODUCT_LESS_THAN_TARGET_TESTS: list[Any] = [
    ([2, 5, 3, 10], 30, [[2], [5], [2, 5], [3], [5, 3], [10]]),
    ([8, 2, 6, 5], 50, [[8], [2], [8, 2], [6], [2, 6], [5], [6, 5]]),
]
TWO_POINTERS_DUTCH_NATIONAL_FLAG_PROBLEM_TESTS: list[Any] = [
    ([1, 0, 2, 1, 0], [0, 0, 1, 1, 2]),
    ([2, 2, 0, 1, 2, 0], [0, 0, 1, 2, 2, 2]),
]
