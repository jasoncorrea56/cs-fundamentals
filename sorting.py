import sys


class SortingAlgorithms:

    @staticmethod
    def selection_sort(nums: list[int]) -> list[int]:
        """
        Selection Sort Function - Ω(n²) | θ(n²) | O(n²)
        :param nums: List of integers.
        :return: Sorted list of integers.
        """
        for i in range(len(nums)-1):
            min_index = i
            for j in range(i+1, len(nums)):
                if nums[j] < nums[min_index]:
                    min_index = j
            nums[min_index], nums[i] = nums[i], nums[min_index]
        return nums

    @staticmethod
    def bubble_sort(nums: list[int]) -> list[int]:
        """
        Bubble Sort Function - Ω(n) | θ(n²) | O(n²)
        :param nums: List of integers.
        :return: Sorted list of integers.
        """
        for i in range(len(nums)-1):
            for j in range(len(nums)-i-1):
                if nums[j] > nums[j+1]:
                    nums[j], nums[j+1] = nums[j+1], nums[j]
        return nums

    @staticmethod
    def insertion_sort(nums: list[int]) -> list[int]:
        """
        Insertion Sort Function - Ω(n) | θ(n²) | O(n²)
        :param nums: List of integers.
        :return: Sorted list of integers.
        """
        for i in range(1, len(nums)):
            key = nums[i]
            j = i-1
            while j >= 0 and nums[j] > key:
                nums[j+1] = nums[j]
                j -= 1
            nums[j+1] = key
        return nums

    def merge_sort(self, nums: list[int]) -> list[int]:
        """
        Merge Sort Function - Ω(n logn(n)) | θ(n logn(n)) | O(n logn(n))
        :param nums: List of integers.
        :return: Sorted list of integers.
        """
        if len(nums) > 1:
            mid = len(nums) // 2
            left = nums[:mid]
            right = nums[mid:]

            self.merge_sort(left)
            self.merge_sort(right)

            i = j = k = 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    nums[k] = left[i]
                    i += 1
                else:
                    nums[k] = right[j]
                    j += 1
                k += 1

            while i < len(left):
                nums[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                nums[k] = right[j]
                j += 1
                k += 1

        return nums

    @staticmethod
    def partition(nums, low, high):
        """
        This function takes last element as pivot, places the pivot element at its
        correct position in sorted array, and places all smaller (smaller than pivot)
        to left of pivot and all greater elements to right of pivot
        :param nums: List of integers
        :param low: Starting index
        :param high: Ending index
        :return:
        """
        i = (low - 1)
        pivot = nums[high]
        for j in range(low, high):
            if nums[j] <= pivot:
                i += 1
                nums[i], nums[j] = nums[j], nums[i]
        nums[i+1], nums[high] = nums[high], nums[i+1]
        return i + 1

    def quick_sort(self, nums: list[int], low: int, high: int) -> list[int]:
        """
        Quick Sort Function - Ω(n logn(n)) | θ(n logn(n)) | O(n²)
        :param nums: List of integers
        :param low: Starting index
        :param high: Ending index
        :return: Sorted list of integers.
        """
        if len(nums) == 1:
            return nums
        if low < high:
            pi = self.partition(nums, low, high)
            self.quick_sort(nums, low, pi - 1)
            self.quick_sort(nums, pi + 1, high)
        return nums

    def heapify(self, nums, n, i):
        """
        Heapify function generates a max heap from the input list
        :param nums: List of integers
        :param n: Length of list
        :param i: Index of root element
        :return:
        """
        largest = i  # Initialize largest as root
        left = 2 * i + 1  # left = 2*i + 1
        right = 2 * i + 2  # right = 2*i + 2

        # See if left child of root exists and is greater than root
        if left < n and nums[i] < nums[left]:
            largest = left
        # See if right child of root exists and is greater than root
        if right < n and nums[largest] < nums[right]:
            largest = right
        # Change root, if needed
        if largest != i:
            nums[i], nums[largest] = nums[largest], nums[i]
            self.heapify(nums, n, largest)  # Heapify the root.

    def heap_sort(self, nums: list[int]) -> list[int]:
        """
        Heap Sort Function - Ω(n logn(n)) | θ(n logn(n)) | O(n logn(n))
        :param nums: List of integers.
        :return: Sorted list of integers.
        """
        n = len(nums)
        # Build a maxheap. Since last parent will be at ((n//2)-1) we can start at that location.
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(nums, n, i)

        # One by one extract elements
        for i in range(n - 1, 0, -1):
            nums[i], nums[0] = nums[0], nums[i]
            self.heapify(nums, i, 0)
        return nums

    @staticmethod
    def counting_sort(nums, exp1):
        """
        A function to do counting sort of nums[] according to the exp1 represented by exp.
        :param nums: List of integers to sort
        :param exp1: Digit on which to sort
        :return:
        """
        n = len(nums)
        output = [0] * n
        count = [0] * 10

        # Store count of occurrences in count[]
        for i in range(0, n):
            index = (nums[i] / exp1)
            count[int(index % 10)] += 1

        # Change count[i] so that count[i] now contains actual position of this exp1 in output array
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Build the output array
        i = n - 1
        while i >= 0:
            index = (nums[i] / exp1)
            output[count[int(index % 10)] - 1] = nums[i]
            count[int(index % 10)] -= 1
            i -= 1

        # Copying the output array to nums[], so that nums now contains sorted numbers
        i = 0
        for i in range(len(nums)):
            nums[i] = output[i]

    def radix_sort(self, nums: list[int]) -> list[int]:
        """
        Radix Sort Function - Ω(nk) | θ(nk) | O(nk)
        :param nums: List of integers.
        :return: Sorted list of integers.
        """
        # Do counting sort for every digit. Instead of passing digit number, pass exp (10^i where i is digit number)
        max1 = max(nums)
        exp = 1
        while max1 / exp > 0:
            self.counting_sort(nums, exp)
            exp *= 10
        return nums

    def bucket_sort(self, nums: list[int]) -> list[int]:
        """
        Bucket Sort Function - Ω(n + k) | θ(n + k) | O(n²)
        :param nums: List of integers.
        :return: Sorted list of integers.
        """
        arr = []
        slot_num = 10  # 10 means 10 slots, each
        # slot's size is 0.1
        for i in range(slot_num):
            arr.append([])

        # Put array elements in different buckets
        for j in nums:
            index_b = int(slot_num * j)
            arr[index_b].append(j)

        # Sort individual buckets
        for i in range(slot_num):
            arr[i] = self.insertion_sort(arr[i])

        # concatenate the result
        k = 0
        for i in range(slot_num):
            for j in range(len(arr[i])):
                nums[k] = arr[i][j]
                k += 1
        return nums

    @staticmethod
    def stalin_sort(nums: list[int]) -> list[int]:
        """
        Stalin Sort Function - Ω(n) | θ(n) | O(n)
        Iterate over the list of integers and eliminate any that are out of order.
        :param nums: Out of order list of integers.
        :return: Sorted in order list of integers.
        """
        previous = -sys.maxsize
        # Convert list to dict for O(1) element access time complexity
        nums_dict = {nums[i]: None for i in range(0, len(nums))}        # O(n)

        # When iterating over a dict you cannot delete from it, so make a copy
        loop_dict = nums_dict.copy()                                    # O(n)

        # Iterate over list eliminating out of order elements
        for num in loop_dict:                                           # O(n)
            if num < previous:                                          # O(1)
                del nums_dict[num]                                      # O(1)
            else:
                previous = num                                          # O(1)

        nums = [i for i in nums_dict]                                   # O(n)
        return nums


class PracticeSortingAlgorithms:

    @staticmethod
    def selection_sort(nums: list[int]) -> list[int]:
        """
        Selection Sort Function - Ω(n²) | θ(n²) | O(n²)
        :param nums: List of integers.
        :return: Sorted list of integers.
        """
        raise NotImplementedError

    @staticmethod
    def bubble_sort(nums: list[int]) -> list[int]:
        """
        Bubble Sort Function - Ω(n) | θ(n²) | O(n²)
        :param nums: List of integers.
        :return: Sorted list of integers.
        """
        raise NotImplementedError

    @staticmethod
    def insertion_sort(nums: list[int]) -> list[int]:
        """
        Insertion Sort Function - Ω(n) | θ(n²) | O(n²)
        :param nums: List of integers.
        :return: Sorted list of integers.
        """
        raise NotImplementedError

    def merge_sort(self, nums: list[int]) -> list[int]:
        """
        Merge Sort Function - Ω(n logn(n)) | θ(n logn(n)) | O(n logn(n))
        :param nums: List of integers.
        :return: Sorted list of integers.
        """
        raise NotImplementedError

    @staticmethod
    def partition(nums, low, high):
        """
        This function takes last element as pivot, places the pivot element at its
        correct position in sorted array, and places all smaller (smaller than pivot)
        to left of pivot and all greater elements to right of pivot
        :param nums: List of integers
        :param low: Starting index
        :param high: Ending index
        :return:
        """
        raise NotImplementedError

    def quick_sort(self, nums: list[int], low: int, high: int) -> list[int]:
        """
        Quick Sort Function - Ω(n logn(n)) | θ(n logn(n)) | O(n²)
        Unimplemented Stub:
        return SORT_QUICK_TESTS[0][1]
        :param nums: List of integers
        :param low: Starting index
        :param high: Ending index
        :return: Sorted list of integers.
        """
        raise NotImplementedError

    def heapify(self, nums, n, i):
        """
        Heapify function generates a max heap from the input list
        :param nums: List of integers
        :param n: Length of list
        :param i: Index of root element
        :return:
        """
        raise NotImplementedError

    def heap_sort(self, nums: list[int]) -> list[int]:
        """
        Heap Sort Function - Ω(n logn(n)) | θ(n logn(n)) | O(n logn(n))
        :param nums: List of integers.
        :return: Sorted list of integers.
        """
        raise NotImplementedError

    @staticmethod
    def counting_sort(nums, exp1):
        """
        A function to do counting sort of nums[] according to the exp1 represented by exp.
        :param nums: List of integers to sort
        :param exp1: Digit on which to sort
        :return:
        """
        raise NotImplementedError

    def radix_sort(self, nums: list[int]) -> list[int]:
        """
        Radix Sort Function - Ω(nk) | θ(nk) | O(nk)
        :param nums: List of integers.
        :return: Sorted list of integers.
        """
        raise NotImplementedError

    def bucket_sort(self, nums: list[int]) -> list[int]:
        """
        Bucket Sort Function - Ω(n + k) | θ(n + k) | O(n²)
        :param nums: List of integers.
        :return: Sorted list of integers.
        """
        raise NotImplementedError

    @staticmethod
    def stalin_sort(nums: list[int]) -> list[int]:
        """
        Stalin Sort Function - Ω(n) | θ(n) | O(n)
        :param nums: Out of order list of integers.
        :return: Sorted in order list of integers.
        """
        raise NotImplementedError
