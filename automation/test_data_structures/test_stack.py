import pytest
from automation.resources.data_structures.stack_data import STACK_EXPECTED_OUTPUT
from data_structures.stack import StackArray, StackLinkedList


class TestStack(object):

    @classmethod
    def setup_class(cls) -> None:
        cls.stack_array = StackArray()
        cls.stack_linked_list = StackLinkedList()

    @pytest.fixture()
    def expected_output(self):
        return STACK_EXPECTED_OUTPUT

    def test_array_push(self):
        result = self.stack_array.push(1)
        result &= self.stack_array.push(2)
        result &= self.stack_array.push(3)
        result &= self.stack_array.push(4)
        assert result is True

    def test_array_peek(self):
        result = self.stack_array.peek()
        assert result == 4

    def test_array_pop(self):
        result = self.stack_array.pop()
        assert result == 4

    def test_array_str(self, expected_output):
        result = self.stack_array.__str__()
        assert result == expected_output

    def test_linked_list_push(self):
        result = self.stack_linked_list.push(1)
        result &= self.stack_linked_list.push(2)
        result &= self.stack_linked_list.push(3)
        result &= self.stack_linked_list.push(4)
        assert result is True

    def test_linked_list_peek(self):
        result = self.stack_linked_list.peek()
        assert result == 4

    def test_linked_list_pop(self):
        result = self.stack_linked_list.pop()
        assert result == 4

    def test_linked_list_str(self, expected_output):
        result = self.stack_linked_list.__str__()
        assert result == expected_output
