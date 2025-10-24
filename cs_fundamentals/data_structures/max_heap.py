import sys


class MaxHeap:
    def __init__(self, heap_size: int) -> None:
        self.real_size = 0
        self.heap_size = heap_size
        self.max_heap = [0] * (heap_size + 1)

    def add(self, element: int) -> bool:
        """
        Add an element to the MaxHeap
        Note: if we use an array to represent the complete binary tree and store the root node at index 1, then the:
            1) index of the parent node of any node is [index of the node / 2]
            2) index of the left child node is [index of the node * 2]
            3) index of the right child node is [index of the node * 2 + 1]
        :param element: Element to add to the MaxHeap
        :return: True if element added successfully, else False
        """
        self.real_size += 1
        if self.real_size > self.heap_size:
            self.real_size -= 1
            print("Add() failed: Too many elements.")
            return False

        self.max_heap[self.real_size] = element  # Add element to the heap
        index = self.real_size  # Index of the newly added element
        parent = index // 2  # Parent index of the newly added element

        # If the newly added element is larger than its parent, swap the parent and new element
        while (self.max_heap[index] > self.max_heap[parent]) and index > 1:
            self.max_heap[parent], self.max_heap[index] = (
                self.max_heap[index],
                self.max_heap[parent],
            )
            index = parent  # Update index of the newly added element to its parent
            parent = index // 2  # Update index of the parent to its parent

        return True

    def pop(self) -> int:
        """
        Remove and return the max element from the top of the MaxHeap
        """
        if self.real_size < 1:
            print("Pop() failed: The MaxHeap is empty.")
            return -sys.maxsize

        popped_element = self.max_heap[1]
        # Move last element to root and shrink
        self.max_heap[1] = self.max_heap[self.real_size]
        self.real_size -= 1

        index = 1
        # Sift down while index has at least a left child
        while index * 2 <= self.real_size:
            left = index * 2
            right = index * 2 + 1

            # Choose larger child (guard if right child doesn't exist)
            largest_child = left
            if right <= self.real_size and self.max_heap[right] > self.max_heap[left]:
                largest_child = right

            # If parent < larger child, swap; otherwise heap property holds
            if self.max_heap[index] < self.max_heap[largest_child]:
                self.max_heap[index], self.max_heap[largest_child] = (
                    self.max_heap[largest_child],
                    self.max_heap[index],
                )
                index = largest_child
            else:
                break

        return popped_element

    def peek(self) -> int:
        """
        Get the top element of the MaxHeap
        :return: Maximum value in the MaxHeap
        """
        if self.real_size < 1:
            print("Peek() failed: The MaxHeap is empty.")
            return -sys.maxsize
        return self.max_heap[1]

    def size(self) -> int:
        """
        Get the number of elements in the MaxHeap
        :return: Number of elements in the MaxHeap
        """
        return self.real_size

    def __str__(self) -> str:
        return str(self.max_heap[1 : self.real_size + 1])


class PracticeMaxHeap:
    def __init__(self, heap_size: int) -> None:
        pass

    def add(self, element: int) -> bool:
        """
        Add an element to the MaxHeap
        :param element: Element to add to the MaxHeap
        :return: True if element added successfully, else False
        """
        raise NotImplementedError

    def pop(self) -> int:
        """
        Remove and return the min element from the top of the MaxHeap
        :return: The minimum value from the MaxHeap
        """
        raise NotImplementedError

    def peek(self) -> int:
        """
        Get the top element of the MaxHeap
        :return: Minimum value in the MaxHeap
        """
        raise NotImplementedError

    def size(self) -> int:
        """
        Get the number of elements in the MaxHeap
        :return: Number of elements in the MaxHeap
        """
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError
