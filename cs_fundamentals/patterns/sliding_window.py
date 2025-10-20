import math


class SlidingWindow:
    @staticmethod
    def avg_subarray_of_size_k(nums: list[int], k: int) -> list[float]:
        """
        Given an array, find the average of all subarrays of ‘K’ contiguous elements
        Brute Force:
            result = []
            for i in range(len(nums) - k + 1):
                _sum = 0.0
                for j in range(i, i + k):
                    _sum += nums[j]
                result.append(_sum / k)
            return result
        :param nums: List of integers
        :param k: Length of subarray
        :return: List of integer averages for subarrays of length K
        """
        result = []
        window_sum = 0
        for end in range(len(nums)):
            window_sum += nums[end]
            if end >= k - 1:
                result.append(window_sum / k)
                window_sum -= nums[end - k + 1]
        return result

    @staticmethod
    def max_subarray_of_size_k(nums: list[int], k: int) -> int:
        """
        Given an array of positive numbers and a positive number ‘k’,
        find the maximum sum of any contiguous subarray of size ‘k’
        Brute Force:
            max_sum = 0
            for i in range(len(nums)-k+1):
                temp_sum = 0
                for j in range(i, i+k):
                    temp_sum += nums[j]
                    if j >= k:
                        max_sum = max(max_sum, temp_sum)
            return max_sum
        :param nums: List of integers
        :param k: Length of subarray
        :return: Integer max sum
        """
        max_sum = win_sum = 0
        for end in range(len(nums)):
            win_sum += nums[end]
            if end >= k - 1:
                max_sum = max(max_sum, win_sum)
                win_sum -= nums[end - k + 1]
        return max_sum

    @staticmethod
    def smallest_subarray_sum_greater_than_s(nums: list[int], s: int) -> int:
        """
        Given an array of positive numbers and a positive number ‘S’,
        find the length of the smallest contiguous subarray whose sum is greater than or equal to ‘S’
        If no such subarray exists, return 0
        Brute Force:
            array_size, min_len = len(nums), len(nums)+1
            for i in range(array_size):
                temp_sum, temp_len = nums[i], 1
                if temp_sum >= s:
                    return 1
                for j in range(i+1, array_size):
                    if temp_sum >= s:
                        min_len = min(temp_len, min_len)
                        break
                    temp_sum += nums[j]
                    temp_len += 1
            return 0 if min_len == array_size+1 else min_len
        :param nums: List of integers
        :param s: Positive integer
        :return: Length of smallest subarray
        """
        min_len = math.inf
        start = window_sum = 0
        for end in range(len(nums)):
            window_sum += nums[end]
            while window_sum >= s:
                min_len = min(min_len, end - start + 1)
                window_sum -= nums[start]
                start += 1
        return 0 if min_len == math.inf else min_len

    @staticmethod
    def longest_substring_with_k_distinct_chars(input_string: str, k: int) -> int:
        """
        Given a string, find the length of the longest substring with no more than K distinct characters.
        Assume K is less than or equal to the length of the given string
        :param input_string: Character string
        :param k: Positive integer
        :return: Length of longest substring with no more than k distinct chars
        """
        sub_len = start = 0
        char_freq = {}
        for end in range(len(input_string)):
            right = input_string[end]
            if right not in char_freq:
                char_freq[right] = 0
            char_freq[right] += 1

            while len(char_freq) > k:
                left = input_string[start]
                char_freq[left] -= 1
                if char_freq[left] == 0:
                    del char_freq[left]
                start += 1
            sub_len = max(sub_len, end - start + 1)
        return sub_len

    @staticmethod
    def fruits_into_baskets(fruit: str) -> int:
        """
        You are visiting a farm to collect fruits. The farm has a single row of fruit trees.
        Given two baskets, and your goal is to pick as much fruit as possible and place in the given baskets.
        Given an array of characters, each character represents a fruit tree.
        The farm has the following restrictions:
            1.  Each basket can have only one type of fruit. There is no limit to how much fruit a basket can hold.
            2.  You can start with any tree, but you can’t skip a tree once started.
            3.  You will pick exactly one fruit from every tree until you have to pick from a third fruit type.
        :param fruit: Character string
        :return: Maximum number of fruits in both baskets
        """
        max_fruit = start = 0
        fruit_freq = {}
        for end in range(len(fruit)):
            right = fruit[end]
            if right not in fruit_freq:
                fruit_freq[right] = 0
            fruit_freq[right] += 1

            while len(fruit_freq) > 2:
                left = fruit[start]
                fruit_freq[left] -= 1
                if fruit_freq[left] == 0:
                    del fruit_freq[left]
                start += 1

            max_fruit = max(max_fruit, end - start + 1)
        return max_fruit

    @staticmethod
    def longest_substring_with_distinct_chars(input_string: str) -> int:
        """
        Given a string, find the length of the longest substring with distinct characters.
        Brute Force:
            def lengthOfLongestSubstring(self, s: str) -> int:
                def check(start, end):
                    chars = [0] * 128
                    for i in range(start, end + 1):
                        c = s[i]
                        chars[ord(c)] += 1
                        if chars[ord(c)] > 1:
                            return False
                    return True
                n = len(s)
                res = 0
                for i in range(n):
                    for j in range(i, n):
                        if check(i, j):
                            res = max(res, j - i + 1)
                return res
        :param input_string: Character string
        :return: Length of longest substring with distinct chars
        """
        start = result = 0
        char_map = {}
        for end in range(len(input_string)):
            end_char = input_string[end]
            if end_char in char_map:
                start = max(start, char_map[end_char] + 1)
            char_map[end_char] = end
            result = max(result, end - start + 1)
        return result

    @staticmethod
    def longest_substring_with_same_letters_after_replacement(input_string: str, k: int) -> int:
        """
        Given a string of lowercase letters, if you are allowed to replace no more than ‘k’ letters
        with any letter, find the length of the longest substring having the same letters after replacement.
        :param input_string: Character string
        :param k: Maximum number of characters to replace
        :return: Length of the longest substring having the same letters after replacement
        """
        start = result = max_repeat = 0
        char_map = {}
        for end in range(len(input_string)):
            end_char = input_string[end]
            if end_char not in char_map:
                char_map[end_char] = 0

            char_map[end_char] += 1
            max_repeat = max(max_repeat, char_map[end_char])

            if (end - start + 1 - max_repeat) > k:
                start_char = input_string[start]
                char_map[start_char] -= 1
                start += 1

            result = max(result, end - start + 1)
        return result

    @staticmethod
    def longest_subarray_with_ones_after_replacement(nums: list[int], k: int) -> int:
        """
        Given an array containing 0s and 1s, replace no more than ‘k’ 0s with 1s,
        then find the length of the longest contiguous subarray having all 1s.
        :param nums: List of 1s and 0s
        :param k: Maximum number of 0s to replace with 1s
        :return: Length of the longest contiguous subarray having all 1s
        """
        start = result = max_ones = 0
        for end in range(len(nums)):
            if nums[end] == 1:
                max_ones += 1

            if (end - start + 1 - max_ones) > k:
                if nums[start] == 1:
                    max_ones -= 1
                start += 1

            result = max(result, end - start + 1)
        return result


class PracticeSlidingWindow:
    @staticmethod
    def avg_subarray_of_size_k(nums: list[int], k: int) -> list[float]:
        """
        Given an array, find the average of all subarrays of ‘K’ contiguous elements
        :param nums: List of integers
        :param k: Length of subarray
        :return: List of float averages for subarrays of length K
        """
        raise NotImplementedError

    @staticmethod
    def max_subarray_of_size_k(nums: list[int], k: int) -> int:
        """
        Given an array of positive numbers and a positive number ‘k’,
        find the maximum sum of any contiguous subarray of size ‘k’
        :param nums: List of integers
        :param k: Length of subarray
        :return: Integer max sum
        """
        raise NotImplementedError

    @staticmethod
    def smallest_subarray_sum_greater_than_s(nums: list[int], s: int) -> int:
        """
        Given an array of positive numbers and a positive number ‘S’,
        find the length of the smallest contiguous subarray whose sum is greater than or equal to ‘S’
        If no such subarray exists, return 0
        :param nums: List of integers
        :param s: Positive integer
        :return: Length of smallest subarray
        """
        raise NotImplementedError

    @staticmethod
    def longest_substring_with_k_distinct_chars(input_string: str, k: int) -> int:
        """
        Given a string, find the length of the longest substring with no more than K distinct characters.
        Assume K is less than or equal to the length of the given string
        :param input_string: Character string
        :param k: Positive integer
        :return: Length of longest substring with no more than k distinct chars
        """
        raise NotImplementedError

    @staticmethod
    def fruits_into_baskets(fruit: str) -> int:
        """
        You are visiting a farm to collect fruits. The farm has a single row of fruit trees.
        Given two baskets, and your goal is to pick as much fruit as possible and place in the given baskets.
        Given an array of characters, each character represents a fruit tree.
        The farm has the following restrictions:
            1.  Each basket can have only one type of fruit. There is no limit to how much fruit a basket can hold.
            2.  You can start with any tree, but you can’t skip a tree once started.
            3.  You will pick exactly one fruit from every tree until you have to pick from a third fruit type.
        :param fruit: Character string
        :return: Maximum number of fruits in both baskets
        """
        raise NotImplementedError

    @staticmethod
    def longest_substring_with_distinct_chars(input_string: str) -> int:
        """
        Given a string, find the length of the longest substring with distinct characters.
        :param input_string: Character string
        :return: Length of longest substring with distinct chars
        """
        raise NotImplementedError

    @staticmethod
    def longest_substring_with_same_letters_after_replacement(input_string: str, k: int) -> int:
        """
        Given a string of lowercase letters, if you are allowed to replace no more than ‘k’ letters
        with any letter, find the length of the longest substring having the same letters after replacement.
        :param input_string: Character string
        :param k: Maximum number of characters to replace
        :return: Length of the longest substring having the same letters after replacement
        """
        raise NotImplementedError

    @staticmethod
    def longest_subarray_with_ones_after_replacement(nums: list[int], k: int) -> int:
        """
        Given an array containing 0s and 1s, replace no more than ‘k’ 0s with 1s,
        then find the length of the longest contiguous subarray having all 1s.
        :param nums: List of 1s and 0s
        :param k: Maximum number of 0s to replace with 1s
        :return: Length of the longest contiguous subarray having all 1s
        """
        raise NotImplementedError
