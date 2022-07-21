import pytest
from automation.resources.patterns.sliding_window_data import SLIDING_WINDOW_AVG_OUTPUT, \
    SLIDING_WINDOW_AVG_NUMS, SLIDING_WINDOW_AVG_K, SLIDING_WINDOW_MAX_SUBARRAY_OF_SIZE_K_TESTS, \
    SLIDING_WINDOW_SMALLEST_SUBARRAY_SUM_GREATER_THAN_S_TESTS, \
    SLIDING_WINDOW_LONGEST_SUBSTRING_WITH_K_DISTINCT_CHARS_TESTS, SLIDING_WINDOW_FRUITS_INTO_BASKETS_TESTS, \
    SLIDING_WINDOW_LONGEST_SUBSTRING_WITH_DISTINCT_CHARS_TESTS, \
    SLIDING_WINDOW_LONGEST_SUBSTRING_WITH_SAME_LETTERS_AFTER_REPLACEMENT_TESTS, \
    SLIDING_WINDOW_LONGEST_SUBARRAY_WITH_ONES_AFTER_REPLACEMENT_TESTS
from patterns.sliding_window import SlidingWindow


class TestSlidingWindow(object):

    @classmethod
    def setup_class(cls) -> None:
        cls.sliding_window = SlidingWindow()

    @pytest.fixture()
    def avg_nums(self):
        return SLIDING_WINDOW_AVG_NUMS

    @pytest.fixture()
    def avg_k(self):
        return SLIDING_WINDOW_AVG_K

    def test_avg_subarray_of_size_k(self, avg_nums, avg_k):
        results = self.sliding_window.avg_subarray_of_size_k(avg_nums, avg_k)
        assert results == SLIDING_WINDOW_AVG_OUTPUT

    @pytest.mark.parametrize("nums, k, output", SLIDING_WINDOW_MAX_SUBARRAY_OF_SIZE_K_TESTS)
    def test_max_subarray_of_size_k(self, nums, k, output):
        results = self.sliding_window.max_subarray_of_size_k(nums, k)
        assert results == output

    @pytest.mark.parametrize("nums, s, output", SLIDING_WINDOW_SMALLEST_SUBARRAY_SUM_GREATER_THAN_S_TESTS)
    def test_smallest_subarray_sum_greater_than_s(self, nums, s, output):
        results = self.sliding_window.smallest_subarray_sum_greater_than_s(nums, s)
        assert results == output

    @pytest.mark.parametrize("input_string, k, output", SLIDING_WINDOW_LONGEST_SUBSTRING_WITH_K_DISTINCT_CHARS_TESTS)
    def test_longest_substring_with_k_distinct_chars(self, input_string, k, output):
        results = self.sliding_window.longest_substring_with_k_distinct_chars(input_string, k)
        assert results == output

    @pytest.mark.parametrize("fruit, output", SLIDING_WINDOW_FRUITS_INTO_BASKETS_TESTS)
    def test_fruits_into_baskets(self, fruit, output):
        results = self.sliding_window.fruits_into_baskets(fruit)
        assert results == output

    @pytest.mark.parametrize("input_string, output", SLIDING_WINDOW_LONGEST_SUBSTRING_WITH_DISTINCT_CHARS_TESTS)
    def test_longest_substring_with_distinct_chars(self, input_string, output):
        results = self.sliding_window.longest_substring_with_distinct_chars(input_string)
        assert results == output

    @pytest.mark.parametrize("input_string, k, output",
                             SLIDING_WINDOW_LONGEST_SUBSTRING_WITH_SAME_LETTERS_AFTER_REPLACEMENT_TESTS)
    def test_longest_substring_with_same_letters_after_replacement(self, input_string, k, output):
        results = self.sliding_window.longest_substring_with_same_letters_after_replacement(input_string, k)
        assert results == output

    @pytest.mark.parametrize("nums, k, output", SLIDING_WINDOW_LONGEST_SUBARRAY_WITH_ONES_AFTER_REPLACEMENT_TESTS)
    def test_longest_subarray_with_ones_after_replacement(self, nums, k, output):
        results = self.sliding_window.longest_subarray_with_ones_after_replacement(nums, k)
        assert results == output
