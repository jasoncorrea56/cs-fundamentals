from __future__ import annotations

from threading import Lock

from cs_fundamentals.data_structures.linked_list_single import Node


class QueueCircularArray:
    def __init__(self, capacity: int) -> None:
        # Allow empty slots to be None so we can clear positions on dequeue.
        self.queue: list[int | None] = [None] * capacity
        self.capacity: int = capacity
        self.size: int = 0
        self.head: int = 0
        self.queue_lock = Lock()

    def __str__(self) -> str:
        return str(list(self.queue))

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

    def dequeue(self) -> int | None:
        if self.is_empty():
            return None
        value = self.peek()
        self.queue[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return value

    def peek(self) -> int | None:
        if self.is_empty():
            return None
        return self.queue[self.head]

    def rear(self) -> int | None:
        if self.is_empty():
            return None
        return self.queue[(self.head + self.size - 1) % self.capacity]


class QueueCircularLinkedList:
    def __init__(self, capacity: int) -> None:
        self.size: int = 0
        self.capacity: int = capacity
        self.head: Node | None = None
        self.tail: Node | None = None

    def __str__(self) -> str:
        result: list[int] = []
        node: Node | None = self.head
        while node is not None:
            result.append(node.value)
            node = node.next
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
            tail = self.tail
            assert tail is not None
            tail.next = node
            self.tail = node
        self.size += 1
        return True

    def dequeue(self) -> int | None:
        if self.is_empty():
            return None
        assert self.head is not None  # for type-checker
        value: int = self.head.value
        self.head = self.head.next
        self.size -= 1
        if self.head is None:
            # Queue now empty; keep tail consistent.
            self.tail = None
        return value

    def peek(self) -> int | None:
        if self.is_empty() or self.head is None:
            return None
        return self.head.value

    def rear(self) -> int | None:
        if self.is_empty() or self.tail is None:
            return None
        return self.tail.value


class PracticeQueueCircularArray:
    def __init__(self, capacity: int) -> None:
        pass

    def __str__(self) -> str:
        raise NotImplementedError

    def is_full(self) -> bool:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    def enqueue(self, value: int) -> bool:
        raise NotImplementedError

    def dequeue(self) -> int | None:
        raise NotImplementedError

    def peek(self) -> int | None:
        raise NotImplementedError

    def rear(self) -> int | None:
        raise NotImplementedError


class PracticeQueueCircularLinkedList:
    def __init__(self, capacity: int) -> None:
        pass

    def __str__(self) -> str:
        raise NotImplementedError

    def is_full(self) -> bool:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    def enqueue(self, value: int) -> bool:
        raise NotImplementedError

    def dequeue(self) -> int | None:
        raise NotImplementedError

    def peek(self) -> int | None:
        raise NotImplementedError

    def rear(self) -> int | None:
        raise NotImplementedError
