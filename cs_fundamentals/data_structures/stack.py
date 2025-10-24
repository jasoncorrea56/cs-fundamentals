from __future__ import annotations

from cs_fundamentals.data_structures.linked_list_single import Node


class StackArray:
    def __init__(self) -> None:
        self.stack: list[int] = []

    def __str__(self) -> str:
        result = list(self.stack)
        result.reverse()
        return str(result)

    def is_empty(self) -> bool:
        return len(self.stack) == 0

    def push(self, item: int) -> bool:
        try:
            self.stack.append(item)
        except Exception:  # pragma: no cover - defensive
            return False
        return True

    def pop(self) -> int | None:
        if self.is_empty():
            return None
        return self.stack.pop()

    def peek(self) -> int | None:
        if self.is_empty():
            return None
        return self.stack[-1]


class StackLinkedList:
    def __init__(self) -> None:
        self.top: Node | None = None

    def __str__(self) -> str:
        result: list[int] = []
        node = self.top
        while node is not None:
            result.append(node.value)
            node = node.next
        return str(result)

    def is_empty(self) -> bool:
        return self.top is None

    def push(self, data: int) -> bool:
        node = Node(data)
        node.next = self.top
        self.top = node
        return True

    def pop(self) -> int | None:
        if self.is_empty():
            return None
        assert self.top is not None  # for type checker
        popped = self.top.value
        self.top = self.top.next
        return popped

    def peek(self) -> int | None:
        if self.is_empty():
            return None
        assert self.top is not None  # for type checker
        return self.top.value


class PracticeStackArray:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    def push(self, item: int) -> bool:
        raise NotImplementedError

    def pop(self) -> int | None:
        raise NotImplementedError

    def peek(self) -> int | None:
        raise NotImplementedError


class PracticeStackLinkedList:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    def push(self, data: int) -> bool:
        raise NotImplementedError

    def pop(self) -> int | None:
        raise NotImplementedError

    def peek(self) -> int | None:
        raise NotImplementedError
