from data_structures.linked_list_single import Node


class FastSlowPointers:
    @staticmethod
    def has_cycle_in_linked_list(head: Node) -> bool:
        """
        Given the head of a linked list, determine if the linked list contains a cycle
        Brute Force:
            visited = set()
            while head:
                if head in visited:
                    return True
                visited.add(head)
                head = head.next
            return False
        :param head: Head node of a Linked List
        :return: True if there is a cycle in the list, otherwise False
        """
        if not head:
            return False
        slow, fast = head, head.next
        while slow != fast:
            if not fast or not fast.next:
                return False
            slow, fast = slow.next, fast.next.next
        else:
            return True

    @staticmethod
    def get_first_node_for_cycle_in_linked_list(head: Node) -> Node | None:
        """
        Given the head of a linked list, return the node where the cycle begins. If there is no cycle, return null
        Brute Force:
            visited = set()
            node = head
            while node:
                if node in visited:
                    return node
                visited.add(node)
                node = node.next
            return None
        :param head: Head node of a Linked List
        :return: The node where the cycle begins if a cycle exists, otherwise null
        """

        def get_intersection() -> Node | None:
            slow = fast = head
            while fast and fast.next:
                slow, fast = slow.next, fast.next.next
                if slow == fast:
                    return slow

        if not head:
            return None

        intersection = get_intersection()
        if not intersection:
            return None

        head_ptr, intersect_ptr = head, intersection
        while head_ptr != intersect_ptr:
            head_ptr, intersect_ptr = head_ptr.next, intersect_ptr.next

        return head_ptr


class PracticeFastSlowPointers:
    @staticmethod
    def has_cycle_in_linked_list(head: Node) -> bool:
        """
        Given the head of a linked list, determine if the linked list contains a cycle
        :param head: Head node of a Linked List
        :return: True if there is a cycle in the list, otherwise False
        """
        raise NotImplementedError

    @staticmethod
    def get_first_node_for_cycle_in_linked_list(head: Node) -> Node | None:
        """
        Given the head of a linked list, return the node where the cycle begins. If there is no cycle, return null
        :param head: Head node of a Linked List
        :return: The node where the cycle begins if a cycle exists, otherwise null
        """
        raise NotImplementedError
