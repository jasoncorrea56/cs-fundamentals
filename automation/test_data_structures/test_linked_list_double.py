import pytest
from automation.resources.data_structures.linked_list_data import (
    DOUBLY_LINKED_LIST_OUTPUT,
)
from data_structures.linked_list_double import DoublyLinkedList


class TestLinkedListDouble:
    @classmethod
    def setup_class(cls) -> None:
        cls.linked_list = DoublyLinkedList()

    @pytest.fixture()
    def expected_output(self) -> list[int]:
        return DOUBLY_LINKED_LIST_OUTPUT

    def test_add_at_head(self) -> None:
        self.linked_list.add_at_head(1)
        assert self.linked_list.head.value == 1
        assert self.linked_list.get(0) == 1

    def test_add_at_index(self, expected_output) -> None:
        self.linked_list.add_at_index(1, 2)
        self.linked_list.add_at_index(2, 3)
        self.linked_list.add_at_index(3, 4)
        self.linked_list.add_at_index(4, 5)
        assert self.linked_list.get_list() == expected_output

    def test_add_at_tail(self, expected_output) -> None:
        self.linked_list.add_at_tail(6)
        assert self.linked_list.get_list() == expected_output + [6]

    def test_delete_at_index(self, expected_output) -> None:
        self.linked_list.delete_at_index(5)
        assert self.linked_list.get_list() == expected_output
