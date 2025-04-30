import pytest
from automation.resources.sorting_data import (
    SORT_AVG_EXPECTED_OUTPUT,
    SORT_MAX_EXPECTED_OUTPUT,
    SORT_SELECTION_TESTS,
    SORT_BUBBLE_TESTS,
    SORT_INSERTION_TESTS,
    SORT_MERGE_TESTS,
    SORT_QUICK_TESTS,
    SORT_HEAP_TESTS,
    SORT_RADIX_TESTS,
    SORT_STALIN_TESTS,
)
from automation.test_sorting import TestSortingAlgorithms
from sorting import PracticeSortingAlgorithms


class TestPracticeSortingAlgorithms(TestSortingAlgorithms):
    @classmethod
    def setup_class(cls) -> None:
        cls.sorter = PracticeSortingAlgorithms()
        cls.avg_expected_output = SORT_AVG_EXPECTED_OUTPUT
        cls.max_expected_output = SORT_MAX_EXPECTED_OUTPUT

    @pytest.mark.parametrize("nums, sorted_nums", SORT_SELECTION_TESTS)
    def test_selection_sort(self, nums, sorted_nums) -> None:
        try:
            super().test_selection_sort(nums, sorted_nums)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize("nums, sorted_nums", SORT_BUBBLE_TESTS)
    def test_bubble_sort(self, nums, sorted_nums) -> None:
        try:
            super().test_bubble_sort(nums, sorted_nums)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize("nums, sorted_nums", SORT_INSERTION_TESTS)
    def test_insertion_sort(self, nums, sorted_nums) -> None:
        try:
            super().test_insertion_sort(nums, sorted_nums)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize("nums, sorted_nums", SORT_MERGE_TESTS)
    def test_merge_sort(self, nums, sorted_nums) -> None:
        try:
            super().test_merge_sort(nums, sorted_nums)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize("nums, sorted_nums", SORT_QUICK_TESTS)
    def test_quick_sort(self, nums, sorted_nums) -> None:
        try:
            super().test_quick_sort(nums, sorted_nums)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize("nums, sorted_nums", SORT_HEAP_TESTS)
    def test_heap_sort(self, nums, sorted_nums) -> None:
        try:
            super().test_heap_sort(nums, sorted_nums)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize("nums, sorted_nums", SORT_RADIX_TESTS)
    def test_radix_sort(self, nums, sorted_nums) -> None:
        try:
            super().test_radix_sort(nums, sorted_nums)
        except NotImplementedError:
            assert True

    def test_bucket_sort(self, bucket_nums, sorted_bucket_nums) -> None:
        try:
            super().test_bucket_sort(bucket_nums, sorted_bucket_nums)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize("nums, inorder_nums", SORT_STALIN_TESTS)
    def test_stalin_sort(self, nums, inorder_nums) -> None:
        try:
            super().test_stalin_sort(nums, inorder_nums)
        except NotImplementedError:
            assert True
