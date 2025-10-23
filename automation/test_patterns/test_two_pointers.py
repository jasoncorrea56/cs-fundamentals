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
from cs_fundamentals.patterns.two_pointers import TwoPointers


class TestTwoPointers:
    @classmethod
    def setup_class(cls) -> None:
        cls.two_ptrs = TwoPointers()

    @pytest.mark.parametrize("nums, target, output", TWO_POINTERS_TWO_SUM_TESTS)
    def test_two_sum(self, nums: list[int], target: int, output: list[int]) -> None:
        results = self.two_ptrs.two_sum(nums, target)
        assert results == output

    @pytest.mark.parametrize("nums, output", TWO_POINTERS_THREE_SUM_TESTS)
    def test_three_sum(self, nums: list[int], output: list[list[int]]) -> None:
        results = self.two_ptrs.three_sum(nums)
        assert results == output

    @pytest.mark.parametrize("nums, output", TWO_POINTERS_REMOVE_DUPLICATES_TESTS)
    def test_remove_duplicates(self, nums: list[int], output: int) -> None:
        test_nums = nums.copy()  # So Practice test doesn't fail
        results = self.two_ptrs.remove_duplicates(test_nums)
        assert results == output

    @pytest.mark.parametrize("nums, key, output", TWO_POINTERS_REMOVE_DUPLICATE_KEY_TESTS)
    def test_remove_duplicate_key(self, nums: list[int], key: int, output: int) -> None:
        test_nums = nums.copy()  # So Practice test doesn't fail
        results = self.two_ptrs.remove_duplicate_key(test_nums, key)
        assert results == output

    @pytest.mark.parametrize("nums, output", TWO_POINTERS_SQUARE_SORTED_ARRAY_TESTS)
    def test_square_sorted_array(self, nums: list[int], output: list[int]) -> None:
        results = self.two_ptrs.square_sorted_array(nums)
        assert results == output

    @pytest.mark.parametrize("nums, target, output", TWO_POINTERS_THREE_SUM_TO_TARGET_TESTS)
    def test_three_sum_to_target(self, nums: list[int], target: int, output: int) -> None:
        results = self.two_ptrs.three_sum_to_target(nums, target)
        assert results == output

    @pytest.mark.parametrize("arr, target, output", TWO_POINTERS_TRIPLETS_WITH_SMALLER_SUM_TESTS)
    def test_triplets_with_smaller_sum(self, arr: list[int], target: int, output: int) -> None:
        results = self.two_ptrs.triplets_with_smaller_sum(arr, target)
        assert results == output

    @pytest.mark.parametrize(
        "arr, target, output",
        TWO_POINTERS_SUBARRAYS_WITH_PRODUCT_LESS_THAN_TARGET_TESTS,
    )
    def test_subarrays_with_product_less_than_target(
        self, arr: list[int], target: int, output: list[list[int]]
    ) -> None:
        results = self.two_ptrs.subarrays_with_product_less_than_target(arr, target)
        assert results == output

    @pytest.mark.parametrize("arr, output", TWO_POINTERS_DUTCH_NATIONAL_FLAG_PROBLEM_TESTS)
    def test_dutch_national_flag_problem(self, arr: list[int], output: list[int]) -> None:
        results = self.two_ptrs.dutch_national_flag_problem(arr)
        assert results == output
