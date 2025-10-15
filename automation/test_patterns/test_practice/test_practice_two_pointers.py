import pytest
from automation.resources.patterns.two_pointers_data import (
    TWO_POINTERS_TWO_SUM_TESTS,
    TWO_POINTERS_REMOVE_DUPLICATES_TESTS,
    TWO_POINTERS_REMOVE_DUPLICATE_KEY_TESTS,
    TWO_POINTERS_SQUARE_SORTED_ARRAY_TESTS,
    TWO_POINTERS_THREE_SUM_TESTS,
    TWO_POINTERS_THREE_SUM_TO_TARGET_TESTS,
    TWO_POINTERS_TRIPLETS_WITH_SMALLER_SUM_TESTS,
    TWO_POINTERS_SUBARRAYS_WITH_PRODUCT_LESS_THAN_TARGET_TESTS,
    TWO_POINTERS_DUTCH_NATIONAL_FLAG_PROBLEM_TESTS,
)
from automation.test_patterns.test_two_pointers import TestTwoPointers
from cs_fundamentals.patterns.two_pointers import PracticeTwoPointers


class TestPracticeTwoPointers(TestTwoPointers):
    @classmethod
    def setup_class(cls) -> None:
        cls.two_ptrs = PracticeTwoPointers()

    @pytest.mark.parametrize("nums, target, output", TWO_POINTERS_TWO_SUM_TESTS)
    def test_two_sum(self, nums, target, output) -> None:
        try:
            super().test_two_sum(nums, target, output)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize("nums, output", TWO_POINTERS_THREE_SUM_TESTS)
    def test_three_sum(self, nums, output) -> None:
        try:
            super().test_three_sum(nums, output)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize("nums, output", TWO_POINTERS_REMOVE_DUPLICATES_TESTS)
    def test_remove_duplicates(self, nums, output) -> None:
        try:
            super().test_remove_duplicates(nums, output)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize(
        "nums, key, output", TWO_POINTERS_REMOVE_DUPLICATE_KEY_TESTS
    )
    def test_remove_duplicate_key(self, nums, key, output) -> None:
        try:
            super().test_remove_duplicate_key(nums, key, output)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize("nums, output", TWO_POINTERS_SQUARE_SORTED_ARRAY_TESTS)
    def test_square_sorted_array(self, nums, output) -> None:
        try:
            super().test_square_sorted_array(nums, output)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize(
        "nums, target, output", TWO_POINTERS_THREE_SUM_TO_TARGET_TESTS
    )
    def test_three_sum_to_target(self, nums, target, output) -> None:
        try:
            super().test_three_sum_to_target(nums, target, output)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize(
        "arr, target, output", TWO_POINTERS_TRIPLETS_WITH_SMALLER_SUM_TESTS
    )
    def test_triplets_with_smaller_sum(self, arr, target, output) -> None:
        try:
            super().test_triplets_with_smaller_sum(arr, target, output)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize(
        "arr, target, output",
        TWO_POINTERS_SUBARRAYS_WITH_PRODUCT_LESS_THAN_TARGET_TESTS,
    )
    def test_subarrays_with_product_less_than_target(self, arr, target, output) -> None:
        try:
            super().test_subarrays_with_product_less_than_target(arr, target, output)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize(
        "arr, output", TWO_POINTERS_DUTCH_NATIONAL_FLAG_PROBLEM_TESTS
    )
    def test_dutch_national_flag_problem(self, arr, output) -> None:
        try:
            super().test_dutch_national_flag_problem(arr, output)
        except NotImplementedError:
            assert True
