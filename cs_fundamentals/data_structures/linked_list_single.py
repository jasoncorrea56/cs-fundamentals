from __future__ import annotations


class Node:
    def __init__(self, data: int) -> None:
        self.value: int = data
        self.next: Node | None = None


class SinglyLinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None

    def get_node(self, index: int) -> Node | None:
        """
        Gets the node at the specified index of the LinkedList
        :param index: Index of the node to retrieve from the LinkedList
        :return: The node at the specified index of the LinkedList
        """
        curr: Node | None = self.head
        for _ in range(index):
            if curr:
                curr = curr.next
        return curr

    def get_tail(self) -> Node | None:
        """
        Gets the last node of the LinkedList
        :return: The last node of the LinkedList (or None if empty)
        """
        tail: Node | None = self.head
        while tail and tail.next:
            tail = tail.next
        return tail

    def get(self, index: int) -> int:
        """
        Gets the value of node at the specified index of the LinkedList
        :param index: Index of the node for which the value will be retrieved from the LinkedList
        :return: The value of the node at the specified index of the LinkedList
        """
        node = self.get_node(index)
        return node.value if node else -1

    def get_list(self) -> list[int]:
        """
        Gets the values of the LinkedList in an array
        :return: A list of values from the LinkedList
        """
        linked_list: list[int] = []
        node: Node | None = self.head
        while node and node.value not in linked_list:
            linked_list.append(node.value)
            node = node.next
        return linked_list

    def add_at_head(self, val: int) -> None:
        """
        Adds new node containing the specified value to the head of the LinkedList
        :param val: Data to insert at the head of the LinkedList
        :return: None
        """
        new_node: Node = Node(val)
        new_node.next = self.head
        self.head = new_node

    def add_at_tail(self, val: int) -> None:
        """
        Adds new node containing the specified value to the tail of the LinkedList
        :param val: Data to insert at the tail of the LinkedList
        :return: None
        """
        if not self.head:
            self.add_at_head(val)
            return
        new_node: Node = Node(val)
        prev_node: Node | None = self.get_tail()
        if prev_node is not None:
            prev_node.next = new_node

    def add_at_index(self, index: int, val: int) -> None:
        """
        Adds new node containing the specified value to the head of the LinkedList
        :param index: Index to insert a new node containing the specified value of the LinkedList
        :param val: Data to insert at the specified index of the LinkedList
        :return: None
        """
        if index == 0:
            self.add_at_head(val)
            return
        prev_node: Node | None = self.get_node(index - 1)
        if not prev_node:
            return
        new_node: Node = Node(val)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_at_index(self, index: int) -> None:
        """
        Deletes the node at the specified index from the LinkedList
        :param index: Index of the node to delete from the LinkedList
        :return: None
        """
        del_node: Node | None = self.get_node(index)
        if not del_node:
            return
        if index == 0:
            self.head = del_node.next
        else:
            prev_node: Node | None = self.get_node(index - 1)
            if prev_node:
                prev_node.next = del_node.next


class PracticeSinglyLinkedList:
    def __init__(self) -> None:
        pass

    def get_node(self, index: int) -> Node | None:
        """
        Gets the node at the specified index of the LinkedList
        :param index: Index of the node to retrieve from the LinkedList
        :return: The node at the specified index of the LinkedList
        """
        raise NotImplementedError

    def get_tail(self) -> Node | None:
        """
        Gets the last node of the LinkedList
        :return: The last node of the LinkedList
        """
        raise NotImplementedError

    def get(self, index: int) -> int:
        """
        Gets the value of node at the specified index of the LinkedList
        :param index: Index of the node for which the value will be retrieved from the LinkedList
        :return: The value of the node at the specified index of the LinkedList
        """
        raise NotImplementedError

    def get_list(self) -> list[int]:
        """
        Gets the values of the LinkedList in an array
        :return: A list of values from the LinkedList
        """
        raise NotImplementedError

    def add_at_head(self, val: int) -> None:
        """
        Adds new node containing the specified value to the head of the LinkedList
        :param val: Data to insert at the head of the LinkedList
        :return: None
        """
        raise NotImplementedError

    def add_at_tail(self, val: int) -> None:
        """
        Adds new node containing the specified value to the tail of the LinkedList
        :param val: Data to insert at the tail of the LinkedList
        :return: None
        """
        raise NotImplementedError

    def add_at_index(self, index: int, val: int) -> None:
        """
        Adds new node containing the specified value to the head of the LinkedList
        :param index: Index to insert a new node containing the specified value of the LinkedList
        :param val: Data to insert at the specified index of the LinkedList
        :return: None
        """
        raise NotImplementedError

    def delete_at_index(self, index: int) -> None:
        """
        Deletes the node at the specified index from the LinkedList
        :param index: Index of the node to delete from the LinkedList
        :return: None
        """
        raise NotImplementedError
