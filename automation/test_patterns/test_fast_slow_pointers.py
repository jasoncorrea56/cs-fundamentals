import pytest
from automation.resources.patterns.fast_slow_pointers_data import (
    FAST_SLOW_POINTERS_OUTPUT,
)
from cs_fundamentals.data_structures.linked_list_single import Node, SinglyLinkedList
from cs_fundamentals.patterns.fast_slow_pointers import FastSlowPointers


class TestFastSlowPointers:
    @classmethod
    def setup_class(cls) -> None:
        cls.fs_pointers = FastSlowPointers()
        cls.linked_list = SinglyLinkedList()

    @pytest.fixture()
    def cycle_first_node(self) -> Node:
        return self.linked_list.get_node(2)

    def test_build_linked_list_cycle(self) -> None:
        self.linked_list.add_at_head(1)
        self.linked_list.add_at_index(1, 2)
        self.linked_list.add_at_index(2, 3)
        self.linked_list.add_at_index(3, 4)
        self.linked_list.add_at_tail(5)
        middle = self.linked_list.get_node(2)
        tail = self.linked_list.get_tail()
        tail.next = middle
        assert self.linked_list.get_list() == FAST_SLOW_POINTERS_OUTPUT

    def test_has_cycle_in_linked_list(self) -> None:
        results = self.fs_pointers.has_cycle_in_linked_list(self.linked_list.head)
        assert results is True

    def test_get_first_node_for_cycle_in_linked_list(self, cycle_first_node: Node) -> None:
        results = self.fs_pointers.get_first_node_for_cycle_in_linked_list(self.linked_list.head)
        assert results == cycle_first_node

    def test_has_cycle_in_linked_list_empty(self) -> None:
        assert FastSlowPointers.has_cycle_in_linked_list(None) is False

    def test_has_cycle_in_linked_list_no_cycle(self) -> None:
        ll = SinglyLinkedList()
        ll.add_at_head(1)
        ll.add_at_tail(2)
        ll.add_at_tail(3)
        assert FastSlowPointers.has_cycle_in_linked_list(ll.head) is False

    def test_get_first_node_for_cycle_head_none(self) -> None:
        assert FastSlowPointers.get_first_node_for_cycle_in_linked_list(None) is None

    def test_get_first_node_for_cycle_no_cycle(self) -> None:
        ll = SinglyLinkedList()
        ll.add_at_head(10)
        ll.add_at_tail(20)
        assert FastSlowPointers.get_first_node_for_cycle_in_linked_list(ll.head) is None
