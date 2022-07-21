import sys


class MinHeap(object):
    def __init__(self, heap_size):
        self.real_size = 0
        self.heap_size = heap_size
        self.min_heap = [0] * (heap_size + 1)

    def add(self, element):
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
        index = self.real_size                   # Index of the newly added element
        parent = index // 2                      # Parent index of the newly added element

        # If the newly added element is smaller than its parent, swap the parent and new element
        while (self.min_heap[index] < self.min_heap[parent]) and index > 1:
            self.min_heap[parent], self.min_heap[index] = self.min_heap[index], self.min_heap[parent]
            index = parent                       # Update index of the newly added element to its parent
            parent = index // 2                  # Update index of the parent to its parent

        return True

    def pop(self):
        """
        Remove and return the min element from the top of the MinHeap
        :return: The minimum value from the MinHeap
        """
        if self.real_size < 1:
            print("Pop() failed: The MinHeap is empty.")
            return sys.maxsize
        else:
            popped_element = self.min_heap[1]
            self.min_heap[1] = self.min_heap[self.real_size]  # Put the last element in the Heap to the top
            self.real_size -= 1                               # Decrement number of elements in the Heap
            index = 1                                         # Index of the popped element

            # While the popped element is not a leaf node
            while index <= (self.real_size // 2):
                left = index * 2        # Get the index for the left child of the popped element
                right = (index * 2)     # Get the index for the right child of the popped element

                # If the popped element is larger than the left or right child, swap values with the smaller of the two
                if (self.min_heap[index] > self.min_heap[left]) or (self.min_heap[index] > self.min_heap[right]):
                    if self.min_heap[left] < self.min_heap[right]:
                        self.min_heap[left], self.min_heap[index] = self.min_heap[index], self.min_heap[left]
                        index = left
                    else:
                        self.min_heap[right], self.min_heap[index] = self.min_heap[index], self.min_heap[right]
                        index = right

            return popped_element

    def peek(self):
        """
        Get the top element of the MinHeap
        :return: Minimum value in the MinHeap
        """
        return self.min_heap[1]

    def size(self):
        """
        Get the number of elements in the MinHeap
        :return: Number of elements in the MinHeap
        """
        return self.real_size

    def __str__(self):
        return str(self.min_heap[1: self.real_size + 1])


class MaxHeap(object):
    def __init__(self, heap_size):
        self.real_size = 0
        self.heap_size = heap_size
        self.max_heap = [0] * (heap_size + 1)

    def add(self, element):
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
        index = self.real_size                   # Index of the newly added element
        parent = index // 2                      # Parent index of the newly added element

        # If the newly added element is larger than its parent, swap the parent and new element
        while (self.max_heap[index] > self.max_heap[parent]) and index > 1:
            self.max_heap[parent], self.max_heap[index] = self.max_heap[index], self.max_heap[parent]
            index = parent                       # Update index of the newly added element to its parent
            parent = index // 2                  # Update index of the parent to its parent

        return True

    def pop(self):
        """
        Remove and return the min element from the top of the MaxHeap
        :return: The minimum value from the MaxHeap
        """
        if self.real_size < 1:
            print("Pop() failed: The MaxHeap is empty.")
            return -sys.maxsize
        else:
            popped_element = self.max_heap[1]
            self.max_heap[1] = self.max_heap[self.real_size]  # Put the last element in the Heap to the top
            self.real_size -= 1                               # Decrement number of elements in the Heap
            index = 1                                         # Index of the popped element

            # While the popped element is not a leaf node
            while index <= (self.real_size // 2):
                left = index * 2        # Get the index for the left child of the popped element
                right = (index * 2)     # Get the index for the right child of the popped element

                # If the popped element is smaller than the left or right child, swap values with the larger of the two
                if (self.max_heap[index] < self.max_heap[left]) or (self.max_heap[index] < self.max_heap[right]):
                    if self.max_heap[left] > self.max_heap[right]:
                        self.max_heap[left], self.max_heap[index] = self.max_heap[index], self.max_heap[left]
                        index = left
                    else:
                        self.max_heap[right], self.max_heap[index] = self.max_heap[index], self.max_heap[right]
                        index = right

            return popped_element

    def peek(self):
        """
        Get the top element of the MaxHeap
        :return: Minimum value in the MaxHeap
        """
        return self.max_heap[1]

    def size(self):
        """
        Get the number of elements in the MaxHeap
        :return: Number of elements in the MaxHeap
        """
        return self.real_size

    def __str__(self):
        return str(self.max_heap[1: self.real_size + 1])


class PracticeMinHeap(object):
    def __init__(self, heap_size):
        pass

    def add(self, element):
        """
        Add an element to the MinHeap
        :param element: Element to add to the MinHeap
        :return: True if element added successfully, else False
        """
        raise NotImplementedError

    def pop(self):
        """
        Remove and return the min element from the top of the MinHeap
        :return: The minimum value from the MinHeap
        """
        raise NotImplementedError

    def peek(self):
        """
        Get the top element of the MinHeap
        :return: Minimum value in the MinHeap
        """
        raise NotImplementedError

    def size(self):
        """
        Get the number of elements in the MinHeap
        :return: Number of elements in the MinHeap
        """
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class PracticeMaxHeap(object):
    def __init__(self, heap_size):
        pass

    def add(self, element):
        """
        Add an element to the MaxHeap
        :param element: Element to add to the MaxHeap
        :return: True if element added successfully, else False
        """
        raise NotImplementedError

    def pop(self):
        """
        Remove and return the min element from the top of the MaxHeap
        :return: The minimum value from the MaxHeap
        """
        raise NotImplementedError

    def peek(self):
        """
        Get the top element of the MaxHeap
        :return: Minimum value in the MaxHeap
        """
        raise NotImplementedError

    def size(self):
        """
        Get the number of elements in the MaxHeap
        :return: Number of elements in the MaxHeap
        """
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError
