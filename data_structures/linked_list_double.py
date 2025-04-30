class Node:
    def __init__(self, data, next_node=None, prev_node=None) -> None:
        self.value = data
        self.next = next_node
        self.prev = prev_node


class DoublyLinkedList:
    def __init__(self) -> None:
        self.head = None

    def get_node(self, index: int) -> Node:
        """
        Gets the node at the specified index of the LinkedList
        :param index: Index of the node to retrieve from the LinkedList
        :return: The node at the specified index of the LinkedList
        """
        curr = self.head
        for i in range(index):
            if curr:
                curr = curr.next
        return curr

    def get_tail(self) -> Node:
        """
        Gets the last node of the LinkedList
        :return: The last node of the LinkedList
        """
        tail = self.head
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

    def get_list(self) -> list:
        """
        Gets the values of the LinkedList in an array
        :return: A list of values from the LinkedList
        """
        linked_list = []
        node = self.head
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
        new_node = Node(val)
        new_node.next = self.head
        if self.head:  #
            self.head.prev = new_node  #
        self.head = new_node
        return

    def add_at_tail(self, val: int) -> None:
        """
        Adds new node containing the specified value to the tail of the LinkedList
        :param val: Data to insert at the tail of the LinkedList
        :return: None
        """
        if not self.head:
            self.add_at_head(val)
            return
        new_node = Node(val)
        prev_node = self.get_tail()
        prev_node.next = new_node
        new_node.prev = prev_node  #
        return

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
        prev_node = self.get_node(index - 1)
        if not prev_node:
            return
        new_node = Node(val)
        next_node = prev_node.next  #
        new_node.prev = prev_node  #
        new_node.next = prev_node.next
        prev_node.next = new_node
        if next_node:  #
            next_node.prev = new_node  #
        return

    def delete_at_index(self, index: int) -> None:
        """
        Deletes the node at the specified index from the LinkedList
        :param index: Index of the node to delete from the LinkedList
        :return: None
        """
        del_node = self.get_node(index)
        if not del_node:
            return
        next_node = del_node.next  #
        prev_node = del_node.prev  #
        if prev_node:  #
            prev_node.next = next_node  #
        else:
            self.head = next_node
        if next_node:
            next_node.prev = prev_node
        return


class PracticeDoublyLinkedList:
    def __init__(self) -> None:
        pass

    def get_node(self, index: int) -> Node:
        """
        Gets the node at the specified index of the LinkedList
        :param index: Index of the node to retrieve from the LinkedList
        :return: The node at the specified index of the LinkedList
        """
        raise NotImplementedError

    def get_tail(self) -> Node:
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

    def get_list(self) -> list:
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
