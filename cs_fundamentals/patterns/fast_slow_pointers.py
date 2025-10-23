from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cs_fundamentals.data_structures.linked_list_single import Node


class FastSlowPointers:
    @staticmethod
    def has_cycle_in_linked_list(head: Node | None) -> bool:
        """
        Given the head of a linked list, determine if the linked list contains a cycle
        :param head: Head node of a Linked List
        :return: True if there is a cycle in the list, otherwise False
        """
        if head is None:
            return False

        slow: Node | None = head
        fast: Node | None = head.next

        while slow is not fast:
            if fast is None or fast.next is None:
                return False
            assert slow is not None  # for type checker
            slow = slow.next
            fast = fast.next.next
        return True

    @staticmethod
    def get_first_node_for_cycle_in_linked_list(head: Node | None) -> Node | None:
        """
        Given the head of a linked list, return the node where the cycle begins.
        If there is no cycle, return None.
        :param head: Head node of a Linked List
        :return: The node where the cycle begins if a cycle exists, otherwise None
        """

        def get_intersection() -> Node | None:
            slow: Node | None = head
            fast: Node | None = head
            while fast is not None and fast.next is not None:
                assert slow is not None  # for type checker
                slow = slow.next
                fast = fast.next.next
                if slow is fast:
                    return slow
            return None

        if head is None:
            return None

        intersection = get_intersection()
        if intersection is None:
            return None

        head_ptr: Node | None = head
        intersect_ptr: Node | None = intersection
        while head_ptr is not intersect_ptr:
            assert head_ptr is not None and intersect_ptr is not None
            head_ptr = head_ptr.next
            intersect_ptr = intersect_ptr.next

        return head_ptr


class PracticeFastSlowPointers:
    @staticmethod
    def has_cycle_in_linked_list(head: Node | None) -> bool:
        """
        Given the head of a linked list, determine if the linked list contains a cycle
        :param head: Head node of a Linked List
        :return: True if there is a cycle in the list, otherwise False
        """
        raise NotImplementedError

    @staticmethod
    def get_first_node_for_cycle_in_linked_list(head: Node | None) -> Node | None:
        """
        Given the head of a linked list, return the node where the cycle begins. If there is no cycle, return null
        :param head: Head node of a Linked List
        :return: The node where the cycle begins if a cycle exists, otherwise null
        """
        raise NotImplementedError
