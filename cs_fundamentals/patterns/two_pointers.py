import math
from collections import deque


class TwoPointers:
    #
    # Easy Difficulty
    #

    @staticmethod
    def two_sum(nums: list[int], target: int) -> list[int]:
        """
        Given an array of sorted numbers and a target sum, find a pair with sum equal to the given target
        Brute Force:
            result = []
            for i in range(len(nums) - 1):
                for j in range(i, len(nums)):
                    if nums[i] + nums[j] == target:
                        result.append(i)
                        result.append(j)
                        return result
            return result
        :param nums: List of integers
        :param target: Target sum
        :return: List of integers that sum to the target value
        """
        result = []
        left, right = 0, len(nums) - 1
        while left < right:
            temp_sum = nums[left] + nums[right]
            if temp_sum == target:
                result.append(left)
                result.append(right)
                return result
            if target > temp_sum:
                left += 1
            else:
                right -= 1
        return result

    @staticmethod
    def three_sum(nums: list[int]) -> list[list[int]]:
        """
        Given an array of unsorted numbers, find all unique triplets that sum to 0.
        :param nums: List of integers
        :return: List of all unique triplets that sum to 0
        """

        def find_pair(x: int, left: int) -> None:
            right = len(nums) - 1
            while left < right:
                y, z = nums[left], nums[right]
                current_sum = y + z
                if current_sum == x:
                    results.append([-x, y, z])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif x > current_sum:
                    left += 1
                else:
                    right -= 1
            return

        nums.sort()
        results = []
        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            find_pair(-nums[i], i + 1)
        return results

    @staticmethod
    def remove_duplicates(nums: list[int]) -> int:
        """
        Given an array of sorted numbers, in-place remove all duplicates, using no extra space.
        After removing the duplicates, return the length of the subarray without duplicates.
        :param nums: Sorted list of integers
        :return: Length of list with duplicates removed
        """
        i, next_non_dupe = 0, 1
        while i < len(nums):
            if nums[i] != nums[next_non_dupe - 1]:
                nums[next_non_dupe] = nums[i]
                next_non_dupe += 1
            i += 1
        return next_non_dupe

    @staticmethod
    def remove_duplicate_key(nums: list[int], key: int) -> int:
        """
        Given an unsorted array of numbers and a target key, remove all instances of the key in-place.
        Return the new length of the array.
        :param nums: Unsorted list of integers
        :param key: Target key to be removed from the list
        :return: Length of list with duplicate keys removed
        """
        next_non_key = 0
        for i in range(len(nums)):
            if nums[i] != key:
                nums[next_non_key] = nums[i]
                next_non_key += 1
        return next_non_key

    @staticmethod
    def square_sorted_array(nums: list[int]) -> list[int]:
        """
        Given a sorted array, create a new array containing the sorted squares of the numbers in the input array.
        :param nums: Sorted list of integers
        :return: Sorted list of the square of the input integers
        """
        n = len(nums)
        left, right, biggest_index = 0, n - 1, n - 1
        squared = [0] * n
        while left <= right:
            left_square = nums[left] * nums[left]
            right_square = nums[right] * nums[right]
            if left_square > right_square:
                squared[biggest_index] = left_square
                left += 1
            else:
                squared[biggest_index] = right_square
                right -= 1
            biggest_index -= 1
        return squared

    #
    # Medium Difficulty
    #

    @staticmethod
    def three_sum_to_target(nums: list[int], target: int) -> int:
        """
        Given an array of unsorted numbers and a target number, find a triplet in the array whose sum is as close to
        the target number as possible. Return the sum of the triplet.
        If there is more than one such triplet, return the sum of the triplet with the smallest sum.
        :param nums: Unsorted list of integers
        :param target: Integer target sum
        :return: Sum of the triplet closest to the target number
        """
        nums.sort()
        smallest_diff = math.inf
        for i in range(len(nums) - 2):
            left = i + 1
            right = len(nums) - 1
            while left < right:
                target_diff = target - nums[i] - nums[left] - nums[right]
                if target_diff == 0:
                    return target
                if abs(target_diff) < abs(smallest_diff) or (
                    abs(target_diff) == abs(smallest_diff) and target_diff > smallest_diff
                ):
                    smallest_diff = target_diff
                if target_diff > 0:
                    left += 1
                else:
                    right -= 1
        return target - smallest_diff

    @staticmethod
    def triplets_with_smaller_sum(arr: list[int], target: int) -> int:
        """
        Given an array of unsorted numbers and a target sum,
        count all triplets such that arr[i] + arr[j] + arr[k] < target where i, j, and k are three different indices.
        Return the triplet count.
        :param arr: Unsorted list of integers
        :param target: Integer target sum
        :return: Count of triplets with sum less than target number
        """

        def search_pair(target: int, first: int) -> int:
            count: int = 0
            left, right = first + 1, len(arr) - 1
            while left < right:
                if arr[left] + arr[right] < target:
                    count += right - left
                    for i in range(right, left, -1):
                        triplets.append([arr[first], arr[left], arr[i]])
                    left += 1
                else:
                    right -= 1
            return count

        arr.sort()
        result: int = 0
        triplets: list[list[int]] = []
        for i in range(len(arr) - 2):
            result += search_pair(target - arr[i], i)
        print(f"\nTriplets = {triplets}")
        return result

    @staticmethod
    def subarrays_with_product_less_than_target(arr: list[int], target: int) -> list[list]:
        """
        Given an array with positive numbers and a positive target number,
        find all contiguous subarrays whose product is less than the target number.
        :param arr: Unsorted list of integers
        :param target: Integer target product
        :return: List of subarrays whose product is less than the target
        """
        n, result = len(arr), []
        left, product = 0, 1
        for right in range(n):
            product *= arr[right]
            while product >= target and left < n:
                product /= arr[left]
                left += 1
            temp = deque()
            for i in range(right, left - 1, -1):
                temp.appendleft(arr[i])
                result.append(list(temp))
        return result

    @staticmethod
    def dutch_national_flag_problem(arr: list[int]) -> list[int]:
        """
        Given an array containing 0s, 1s and 2s, sort the array in-place.
        Treat numbers of the array as objects (can’t count 0s, 1s, and 2s to recreate the array)
        :param arr: Unsorted list of 0s, 1s, & 2s
        :return: Sorted list of 0s, 1s, & 2s
        """
        i, low, high = 0, 0, len(arr) - 1
        while i <= high:
            if arr[i] == 0:
                arr[i], arr[low] = arr[low], arr[i]
                i += 1
                low += 1
            elif arr[i] == 1:
                i += 1
            else:
                arr[i], arr[high] = arr[high], arr[i]
                high -= 1
        return arr


class PracticeTwoPointers:
    #
    # Easy Difficulty
    #

    @staticmethod
    def two_sum(nums: list[int], target: int) -> list[int]:
        """
        Given an array of sorted numbers and a target sum, find a pair with sum equal to the given target
        :param nums: List of integers
        :param target: Target sum
        :return: List of integers that sum to the target value
        """
        raise NotImplementedError

    @staticmethod
    def three_sum(nums: list[int]) -> list[list[int]]:
        """
        Given an array of unsorted numbers, find all unique triplets that sum to 0.
        :param nums: List of integers
        :return: List of all unique triplets that sum to 0
        """
        raise NotImplementedError

    @staticmethod
    def remove_duplicates(nums: list[int]) -> int:
        """
        Given an array of sorted numbers, in-place remove all duplicates, using no extra space.
        After removing the duplicates, return the length of the subarray without duplicates.
        :param nums: Sorted list of integers
        :return: Length of list with duplicates removed
        """
        raise NotImplementedError

    @staticmethod
    def remove_duplicate_key(nums: list[int], key: int) -> int:
        """
        Given an unsorted array of numbers and a target key, remove all instances of the key in-place.
        Return the new length of the array.
        :param nums: Unsorted list of integers
        :param key: Target key to be removed from the list
        :return: Length of list with duplicate keys removed
        """
        raise NotImplementedError

    @staticmethod
    def square_sorted_array(nums: list[int]) -> list[int]:
        """
        Given a sorted array, create a new array containing the sorted squares of the numbers in the input array.
        :param nums: Sorted list of integers
        :return: Sorted list of the square of the input integers
        """
        raise NotImplementedError

    #
    # Medium Difficulty
    #

    @staticmethod
    def three_sum_to_target(nums: list[int], target: int) -> int:
        """
        Given an array of unsorted numbers and a target number, find a triplet in the array whose sum is as close to
        the target number as possible. Return the sum of the triplet.
        If there is more than one such triplet, return the sum of the triplet with the smallest sum.
        :param nums: Unsorted list of integers
        :param target: Integer target sum
        :return: Sum of the triplet closest to the target number
        """
        raise NotImplementedError

    @staticmethod
    def triplets_with_smaller_sum(arr: list[int], target: int) -> int:
        """
        Given an array of unsorted numbers and a target sum,
        count all triplets such that arr[i] + arr[j] + arr[k] < target where i, j, and k are three different indices.
        Return the triplet count.
        :param arr: Unsorted list of integers
        :param target: Integer target sum
        :return: Count of triplets with sum less than target number
        """
        raise NotImplementedError

    @staticmethod
    def subarrays_with_product_less_than_target(arr: list[int], target: int) -> list[list]:
        """
        Given an array with positive numbers and a positive target number,
        find all contiguous subarrays whose product is less than the target number.
        :param arr: Unsorted list of integers
        :param target: Integer target product
        :return: List of subarrays whose product is less than the target
        """
        raise NotImplementedError

    @staticmethod
    def dutch_national_flag_problem(arr: list[int]) -> list[int]:
        """
        Given an array containing 0s, 1s and 2s, sort the array in-place.
        Treat numbers of the array as objects (can’t count 0s, 1s, and 2s to recreate the array)
        :param arr: Unsorted list of 0s, 1s, & 2s
        :return: Sorted list of 0s, 1s, & 2s
        """
        raise NotImplementedError
