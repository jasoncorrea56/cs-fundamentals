import sys


class MinHeap:
    def __init__(self, heap_size: int) -> None:
        self.real_size: int = 0
        self.heap_size: int = heap_size
        self.min_heap: list[int] = [0] * (heap_size + 1)

    def add(self, element: int) -> bool:
        """
        Add an element to the MinHeap
        Note: if we use an array to represent the complete binary tree and store the root node at index 1, then the:
            1) index of the parent node of any node is [index of the node / 2]
            2) index of the left child node is [index of the node * 2]
            3) index of the right child node is [index of the node * 2 + 1]
        :param element: Element to add to the MinHeap
        :return: True if element added successfully, else False
        """
        self.real_size += 1
        if self.real_size > self.heap_size:
            self.real_size -= 1
            print("Add() failed: Too many elements.")
            return False

        self.min_heap[self.real_size] = element  # Add element to the heap
        index = self.real_size  # Index of the newly added element
        parent = index // 2  # Parent index of the newly added element

        # If the newly added element is smaller than its parent, swap the parent and new element
        while (self.min_heap[index] < self.min_heap[parent]) and index > 1:
            self.min_heap[parent], self.min_heap[index] = (
                self.min_heap[index],
                self.min_heap[parent],
            )
            index = parent  # Update index of the newly added element to its parent
            parent = index // 2  # Update index of the parent to its parent

        return True

    def pop(self) -> int:
        """
        Remove and return the min element from the top of the MinHeap.
        """
        if self.real_size < 1:
            print("Pop() failed: The MinHeap is empty.")
            return sys.maxsize

        popped_element: int = self.min_heap[1]
        # Move last element to root and shrink
        self.min_heap[1] = self.min_heap[self.real_size]
        self.real_size -= 1

        index = 1
        # Sift down while index has at least a left child
        while index * 2 <= self.real_size:
            left = index * 2
            right = index * 2 + 1

            # Choose smaller child (guard if right child doesn't exist)
            smallest_child = left
            if right <= self.real_size and self.min_heap[right] < self.min_heap[left]:
                smallest_child = right

            # If parent > smaller child, swap; otherwise heap property holds
            if self.min_heap[index] > self.min_heap[smallest_child]:
                self.min_heap[index], self.min_heap[smallest_child] = (
                    self.min_heap[smallest_child],
                    self.min_heap[index],
                )
                index = smallest_child
            else:
                break

        return popped_element

    def peek(self) -> int:
        """
        Get the top element of the MinHeap.
        :return: Minimum value in the MinHeap
        """
        if self.real_size < 1:
            print("Peek() failed: The MinHeap is empty.")
            return sys.maxsize
        return self.min_heap[1]

    def size(self) -> int:
        """
        Get the number of elements in the MinHeap
        :return: Number of elements in the MinHeap
        """
        return self.real_size

    def __str__(self) -> str:
        return str(self.min_heap[1 : self.real_size + 1])


class PracticeMinHeap:
    def __init__(self, heap_size: int) -> None:
        pass

    def add(self, element: int) -> bool:
        """
        Add an element to the MinHeap
        :param element: Element to add to the MinHeap
        :return: True if element added successfully, else False
        """
        raise NotImplementedError

    def pop(self) -> int:
        """
        Remove and return the min element from the top of the MinHeap
        :return: The minimum value from the MinHeap
        """
        raise NotImplementedError

    def peek(self) -> int:
        """
        Get the top element of the MinHeap
        :return: Minimum value in the MinHeap
        """
        raise NotImplementedError

    def size(self) -> int:
        """
        Get the number of elements in the MinHeap
        :return: Number of elements in the MinHeap
        """
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError
