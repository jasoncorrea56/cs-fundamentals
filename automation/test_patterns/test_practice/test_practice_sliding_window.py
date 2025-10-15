import pytest
from automation.resources.patterns.sliding_window_data import (
    SLIDING_WINDOW_MAX_SUBARRAY_OF_SIZE_K_TESTS,
    SLIDING_WINDOW_SMALLEST_SUBARRAY_SUM_GREATER_THAN_S_TESTS,
    SLIDING_WINDOW_LONGEST_SUBSTRING_WITH_K_DISTINCT_CHARS_TESTS,
    SLIDING_WINDOW_FRUITS_INTO_BASKETS_TESTS,
    SLIDING_WINDOW_LONGEST_SUBSTRING_WITH_DISTINCT_CHARS_TESTS,
    SLIDING_WINDOW_LONGEST_SUBSTRING_WITH_SAME_LETTERS_AFTER_REPLACEMENT_TESTS,
    SLIDING_WINDOW_LONGEST_SUBARRAY_WITH_ONES_AFTER_REPLACEMENT_TESTS,
)
from automation.test_patterns.test_sliding_window import TestSlidingWindow
from cs_fundamentals.patterns.sliding_window import PracticeSlidingWindow


class TestPracticeSlidingWindow(TestSlidingWindow):
    @classmethod
    def setup_class(cls) -> None:
        cls.sliding_window = PracticeSlidingWindow()

    @pytest.mark.usefixtures("avg_nums", "avg_k")
    def test_avg_subarray_of_size_k(self, avg_nums, avg_k) -> None:
        try:
            super().test_avg_subarray_of_size_k(avg_nums, avg_k)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize(
        "nums, k, output", SLIDING_WINDOW_MAX_SUBARRAY_OF_SIZE_K_TESTS
    )
    def test_max_subarray_of_size_k(self, nums, k, output) -> None:
        try:
            super().test_max_subarray_of_size_k(nums, k, output)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize(
        "nums, s, output", SLIDING_WINDOW_SMALLEST_SUBARRAY_SUM_GREATER_THAN_S_TESTS
    )
    def test_smallest_subarray_sum_greater_than_s(self, nums, s, output) -> None:
        try:
            super().test_smallest_subarray_sum_greater_than_s(nums, s, output)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize(
        "input_string, k, output",
        SLIDING_WINDOW_LONGEST_SUBSTRING_WITH_K_DISTINCT_CHARS_TESTS,
    )
    def test_longest_substring_with_k_distinct_chars(
        self, input_string, k, output
    ) -> None:
        try:
            super().test_longest_substring_with_k_distinct_chars(
                input_string, k, output
            )
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize("fruit, output", SLIDING_WINDOW_FRUITS_INTO_BASKETS_TESTS)
    def test_fruits_into_baskets(self, fruit, output) -> None:
        try:
            super().test_fruits_into_baskets(fruit, output)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize(
        "input_string, output",
        SLIDING_WINDOW_LONGEST_SUBSTRING_WITH_DISTINCT_CHARS_TESTS,
    )
    def test_longest_substring_with_distinct_chars(self, input_string, output) -> None:
        try:
            super().test_longest_substring_with_distinct_chars(input_string, output)
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize(
        "input_string, k, output",
        SLIDING_WINDOW_LONGEST_SUBSTRING_WITH_SAME_LETTERS_AFTER_REPLACEMENT_TESTS,
    )
    def test_longest_substring_with_same_letters_after_replacement(
        self, input_string, k, output
    ) -> None:
        try:
            super().test_longest_substring_with_same_letters_after_replacement(
                input_string, k, output
            )
        except NotImplementedError:
            assert True

    @pytest.mark.parametrize(
        "nums, k, output",
        SLIDING_WINDOW_LONGEST_SUBARRAY_WITH_ONES_AFTER_REPLACEMENT_TESTS,
    )
    def test_longest_subarray_with_ones_after_replacement(
        self, nums, k, output
    ) -> None:
        try:
            super().test_longest_subarray_with_ones_after_replacement(nums, k, output)
        except NotImplementedError:
            assert True
