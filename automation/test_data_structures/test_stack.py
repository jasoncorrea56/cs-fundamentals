import pytest
from automation.resources.data_structures.stack_data import STACK_EXPECTED_OUTPUT
from cs_fundamentals.data_structures.stack import (
    StackArray,
    StackLinkedList,
)


class TestStack:
    @classmethod
    def setup_class(cls) -> None:
        cls.stack_array = StackArray()
        cls.stack_linked_list = StackLinkedList()

    @pytest.fixture()
    def expected_output(self) -> list[int]:
        return STACK_EXPECTED_OUTPUT

    # ----------------- StackArray Tests -----------------

    def test_array_push(self) -> None:
        result = self.stack_array.push(1)
        result &= self.stack_array.push(2)
        result &= self.stack_array.push(3)
        result &= self.stack_array.push(4)
        assert result is True

    def test_array_peek(self) -> None:
        result = self.stack_array.peek()
        assert result == 4

    def test_array_pop(self) -> None:
        result = self.stack_array.pop()
        assert result == 4

    def test_array_str(self, expected_output: str) -> None:
        result = self.stack_array.__str__()
        assert result == expected_output

    def test_array_pop_empty_returns_none(self) -> None:
        s = StackArray()
        assert s.pop() is None

    def test_array_peek_empty_returns_none(self) -> None:
        s = StackArray()
        assert s.peek() is None

    def test_array_str_empty(self) -> None:
        s = StackArray()
        assert str(s) == "[]"

    # ----------------- StackLinkedList Tests -----------------

    def test_linked_list_push(self) -> None:
        result = self.stack_linked_list.push(1)
        result &= self.stack_linked_list.push(2)
        result &= self.stack_linked_list.push(3)
        result &= self.stack_linked_list.push(4)
        assert result is True

    def test_linked_list_peek(self) -> None:
        result = self.stack_linked_list.peek()
        assert result == 4

    def test_linked_list_pop(self) -> None:
        result = self.stack_linked_list.pop()
        assert result == 4

    def test_linked_list_str(self, expected_output: str) -> None:
        result = self.stack_linked_list.__str__()
        assert result == expected_output

    def test_linked_list_pop_empty_returns_none(self) -> None:
        s = StackLinkedList()
        assert s.pop() is None

    def test_linked_list_peek_empty_returns_none(self) -> None:
        s = StackLinkedList()
        assert s.peek() is None

    def test_linked_list_pop_single_element_makes_empty(self) -> None:
        s = StackLinkedList()
        assert s.push(42) is True
        assert s.pop() == 42
        assert s.is_empty() is True

    def test_linked_list_str_empty(self) -> None:
        s = StackLinkedList()
        assert str(s) == "[]"
