from data_structures.linked_list_single import Node


class StackArray:
    def __init__(self) -> None:
        self.stack = []

    def __str__(self) -> str:
        result = list(self.stack)
        result.reverse()
        return str(result)

    def is_empty(self) -> bool:
        return len(self.stack) == 0

    def push(self, item) -> bool:
        try:
            self.stack.append(item)
        except Exception:
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
        self.top = None

    def __str__(self) -> str:
        result = []
        node = self.top
        while True:
            result.append(node.value)
            node = node.next
            if not node:
                break
        return str(result)

    def is_empty(self) -> bool:
        return not self.top

    def push(self, data) -> bool:
        node = Node(data)
        node.next = self.top
        self.top = node
        return True

    def pop(self) -> int | None:
        if self.is_empty():
            return None
        popped = self.top.value
        self.top = self.top.next
        return popped

    def peek(self) -> int | None:
        if self.is_empty():
            return None
        return self.top.value


class PracticeStackArray:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    def push(self, item) -> bool:
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

    def push(self, data) -> bool:
        raise NotImplementedError

    def pop(self) -> int | None:
        raise NotImplementedError

    def peek(self) -> int | None:
        raise NotImplementedError
