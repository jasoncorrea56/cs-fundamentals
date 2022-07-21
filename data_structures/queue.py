from data_structures.linked_list_single import Node
from threading import Lock
from typing import Optional


class QueueCircularArray(object):
    def __init__(self, capacity: int):
        self.queue = [0]*capacity
        self.capacity = capacity
        self.size = 0
        self.head = 0
        self.queue_lock = Lock()

    def __str__(self):
        return str([x for x in self.queue])

    def is_full(self) -> bool:
        return self.size == self.capacity

    def is_empty(self) -> bool:
        return self.size == 0

    def enqueue(self, value: int) -> bool:
        with self.queue_lock:
            if self.is_full():
                return False
            self.queue[(self.head + self.size) % self.capacity] = value
            self.size += 1
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        value = self.peek()
        self.queue[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return value

    def peek(self) -> Optional[int]:
        if self.is_empty():
            return None
        return self.queue[self.head]

    def rear(self) -> Optional[int]:
        if self.is_empty():
            return None
        return self.queue[(self.head + self.size - 1) % self.capacity]


class QueueCircularLinkedList(object):
    def __init__(self, capacity: int):
        self.size = 0
        self.capacity = capacity
        self.head = None
        self.tail = None

    def __str__(self):
        result = []
        node = self.head
        while True:
            result.append(node.value)
            node = node.next
            if not node:
                break
        return str(result)

    def is_full(self) -> bool:
        return self.size == self.capacity

    def is_empty(self) -> bool:
        return self.size == 0

    def enqueue(self, value: int) -> bool:
        if self.is_full():
            return False

        if self.is_empty():
            self.head = Node(value)
            self.tail = self.head
        else:
            node = Node(value)
            self.tail.next = node
            self.tail = node
        self.size += 1
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        value = self.peek()
        self.head.value = None
        self.head = self.head.next
        self.size -= 1
        return value

    def peek(self) -> Optional[int]:
        if self.is_empty():
            return None
        return self.head.value

    def rear(self) -> Optional[int]:
        if self.is_empty():
            return None
        return self.tail.value


class PracticeQueueCircularArray(object):
    def __init__(self, capacity: int):
        pass

    def __str__(self):
        raise NotImplementedError

    def is_full(self) -> bool:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    def enqueue(self, value: int) -> bool:
        raise NotImplementedError

    def dequeue(self):
        raise NotImplementedError

    def peek(self) -> Optional[int]:
        raise NotImplementedError

    def rear(self) -> Optional[int]:
        raise NotImplementedError


class PracticeQueueCircularLinkedList(object):
    def __init__(self, capacity: int):
        pass

    def __str__(self):
        raise NotImplementedError

    def is_full(self) -> bool:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    def enqueue(self, value: int) -> bool:
        raise NotImplementedError

    def dequeue(self):
        raise NotImplementedError

    def peek(self) -> Optional[int]:
        raise NotImplementedError

    def rear(self) -> Optional[int]:
        raise NotImplementedError
