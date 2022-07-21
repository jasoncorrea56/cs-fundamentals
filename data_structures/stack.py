from data_structures.linked_list_single import Node


class StackArray(object):
    def __init__(self):
        self.stack = []

    def __str__(self):
        result = [x for x in self.stack]
        result.reverse()
        return str(result)

    def is_empty(self):
        return len(self.stack) == 0

    def push(self, item):
        try:
            self.stack.append(item)
        except Exception:
            return False
        return True

    def pop(self):
        if self.is_empty():
            return None
        return self.stack.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.stack[-1]


class StackLinkedList(object):
    def __init__(self):
        self.top = None

    def __str__(self):
        result = []
        node = self.top
        while True:
            result.append(node.value)
            node = node.next
            if not node:
                break
        return str(result)

    def is_empty(self):
        return not self.top

    def push(self, data):
        node = Node(data)
        node.next = self.top
        self.top = node
        return True

    def pop(self):
        if self.is_empty():
            return None
        popped = self.top.value
        self.top = self.top.next
        return popped

    def peek(self):
        if self.is_empty():
            return None
        return self.top.value


class PracticeStackArray(object):
    def __init__(self):
        pass

    def __str__(self):
        raise NotImplementedError

    def is_empty(self):
        raise NotImplementedError

    def push(self, item):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def peek(self):
        raise NotImplementedError


class PracticeStackLinkedList(object):
    def __init__(self):
        pass

    def __str__(self):
        raise NotImplementedError

    def is_empty(self):
        raise NotImplementedError

    def push(self, data):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def peek(self):
        raise NotImplementedError
