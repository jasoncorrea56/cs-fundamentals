import pytest
from automation.resources.patterns.fast_slow_pointers_data import (
    FAST_SLOW_POINTERS_OUTPUT,
)
from data_structures.linked_list_single import SinglyLinkedList
from patterns.fast_slow_pointers import FastSlowPointers


class TestFastSlowPointers(object):
    @classmethod
    def setup_class(cls) -> None:
        cls.fs_pointers = FastSlowPointers()
        cls.linked_list = SinglyLinkedList()

    @pytest.fixture()
    def cycle_first_node(self):
        return self.linked_list.get_node(2)

    def test_build_linked_list_cycle(self):
        self.linked_list.add_at_head(1)
        self.linked_list.add_at_index(1, 2)
        self.linked_list.add_at_index(2, 3)
        self.linked_list.add_at_index(3, 4)
        self.linked_list.add_at_tail(5)
        middle = self.linked_list.get_node(2)
        tail = self.linked_list.get_tail()
        tail.next = middle
        assert self.linked_list.get_list() == FAST_SLOW_POINTERS_OUTPUT

    def test_has_cycle_in_linked_list(self):
        results = self.fs_pointers.has_cycle_in_linked_list(self.linked_list.head)
        assert results is True

    def test_get_first_node_for_cycle_in_linked_list(self, cycle_first_node):
        results = self.fs_pointers.get_first_node_for_cycle_in_linked_list(
            self.linked_list.head
        )
        assert results == cycle_first_node
