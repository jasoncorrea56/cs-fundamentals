import pytest
from automation.resources.sorting_data import (
    SORT_AVG_EXPECTED_OUTPUT,
    SORT_MAX_EXPECTED_OUTPUT,
    SORT_X,
    SORT_Y,
    SORT_BUCKET_NUMS,
    SORT_SORTED_BUCKET_NUMS_OUTPUT,
    SORT_SELECTION_TESTS,
    SORT_BUBBLE_TESTS,
    SORT_INSERTION_TESTS,
    SORT_MERGE_TESTS,
    SORT_QUICK_TESTS,
    SORT_HEAP_TESTS,
    SORT_RADIX_TESTS,
    SORT_STALIN_TESTS,
)

from cs_fundamentals.patterns.sorting import SortingAlgorithms


class TestSortingAlgorithms:
    @classmethod
    def setup_class(cls) -> None:
        cls.sorter = SortingAlgorithms()
        cls.avg_expected_output = SORT_AVG_EXPECTED_OUTPUT
        cls.max_expected_output = SORT_MAX_EXPECTED_OUTPUT

    @pytest.fixture()
    def x(self) -> int:
        return SORT_X

    @pytest.fixture()
    def y(self) -> int:
        return SORT_Y

    @pytest.fixture()
    def bucket_nums(self) -> list[float]:
        return SORT_BUCKET_NUMS

    @pytest.fixture()
    def sorted_bucket_nums(self) -> list[float]:
        return SORT_SORTED_BUCKET_NUMS_OUTPUT

    @pytest.mark.parametrize("nums, sorted_nums", SORT_SELECTION_TESTS)
    def test_selection_sort(self, nums, sorted_nums) -> None:
        results = self.sorter.selection_sort(nums)
        assert results == sorted_nums

    @pytest.mark.parametrize("nums, sorted_nums", SORT_BUBBLE_TESTS)
    def test_bubble_sort(self, nums, sorted_nums) -> None:
        results = self.sorter.bubble_sort(nums)
        assert results == sorted_nums

    @pytest.mark.parametrize("nums, sorted_nums", SORT_INSERTION_TESTS)
    def test_insertion_sort(self, nums, sorted_nums) -> None:
        results = self.sorter.insertion_sort(nums)
        assert results == sorted_nums

    @pytest.mark.parametrize("nums, sorted_nums", SORT_MERGE_TESTS)
    def test_merge_sort(self, nums, sorted_nums) -> None:
        results = self.sorter.merge_sort(nums)
        assert results == sorted_nums

    @pytest.mark.parametrize("nums, sorted_nums", SORT_QUICK_TESTS)
    def test_quick_sort(self, nums, sorted_nums) -> None:
        results = self.sorter.quick_sort(nums, 0, len(nums) - 1)
        assert results == sorted_nums

    @pytest.mark.parametrize("nums, sorted_nums", SORT_HEAP_TESTS)
    def test_heap_sort(self, nums, sorted_nums) -> None:
        results = self.sorter.heap_sort(nums)
        assert results == sorted_nums

    @pytest.mark.parametrize("nums, sorted_nums", SORT_RADIX_TESTS)
    def test_radix_sort(self, nums, sorted_nums) -> None:
        results = self.sorter.radix_sort(nums)
        assert results == sorted_nums

    def test_bucket_sort(self, bucket_nums, sorted_bucket_nums) -> None:
        results = self.sorter.bucket_sort(bucket_nums)
        assert results == sorted_bucket_nums

    @pytest.mark.parametrize("nums, inorder_nums", SORT_STALIN_TESTS)
    def test_stalin_sort(self, nums, inorder_nums) -> None:
        results = self.sorter.stalin_sort(nums)
        assert results == inorder_nums
