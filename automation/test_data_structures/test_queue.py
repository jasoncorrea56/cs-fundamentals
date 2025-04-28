import pytest
from automation.resources.data_structures.queue_data import (
    QUEUE_ARRAY_OUTPUT,
    QUEUE_LINKED_LIST_OUTPUT,
)
from data_structures.queue import QueueCircularArray, QueueCircularLinkedList


class TestQueue(object):
    @classmethod
    def setup_class(cls) -> None:
        cls.queue_array = QueueCircularArray(4)
        cls.queue_linked_list = QueueCircularLinkedList(4)

    @pytest.fixture()
    def array_output(self):
        return QUEUE_ARRAY_OUTPUT

    @pytest.fixture()
    def linked_list_output(self):
        return QUEUE_LINKED_LIST_OUTPUT

    def test_array_enqueue(self):
        result = self.queue_array.enqueue(1)
        result &= self.queue_array.enqueue(2)
        result &= self.queue_array.enqueue(3)
        result &= self.queue_array.enqueue(4)
        assert result is True

    def test_array_peek(self):
        result = self.queue_array.peek()
        assert result == 1

    def test_array_rear(self):
        result = self.queue_array.rear()
        assert result == 4

    def test_array_dequeue(self):
        result = self.queue_array.dequeue()
        assert result == 1

    def test_array_is_empty(self):
        result = self.queue_array.is_empty()
        assert result is False

    def test_array_is_full(self):
        result = self.queue_array.is_full()
        assert result is False

    def test_array_str(self, array_output):
        result = self.queue_array.__str__()
        assert result == array_output

    def test_linked_list_enqueue(self):
        result = self.queue_linked_list.enqueue(1)
        result &= self.queue_linked_list.enqueue(2)
        result &= self.queue_linked_list.enqueue(3)
        result &= self.queue_linked_list.enqueue(4)
        assert result is True

    def test_linked_list_peek(self):
        result = self.queue_linked_list.peek()
        assert result == 1

    def test_linked_list_rear(self):
        result = self.queue_linked_list.rear()
        assert result == 4

    def test_linked_list_dequeue(self):
        result = self.queue_linked_list.dequeue()
        assert result == 1

    def test_linked_list_is_empty(self):
        result = self.queue_linked_list.is_empty()
        assert result is False

    def test_linked_list_is_full(self):
        result = self.queue_linked_list.is_full()
        assert result is False

    def test_linked_list_str(self, linked_list_output):
        result = self.queue_linked_list.__str__()
        assert result == linked_list_output
