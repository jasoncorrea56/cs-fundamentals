import pytest
from automation.resources.data_structures.queue_data import (
    QUEUE_ARRAY_OUTPUT,
    QUEUE_LINKED_LIST_OUTPUT,
)
from cs_fundamentals.data_structures.queue import (
    QueueCircularArray,
    QueueCircularLinkedList,
)


class TestQueue:
    @classmethod
    def setup_class(cls) -> None:
        cls.queue_array = QueueCircularArray(4)
        cls.queue_linked_list = QueueCircularLinkedList(4)

    @pytest.fixture()
    def array_output(self) -> list[None | int]:
        return QUEUE_ARRAY_OUTPUT

    @pytest.fixture()
    def linked_list_output(self) -> list[int]:
        return QUEUE_LINKED_LIST_OUTPUT

    def test_array_enqueue(self) -> None:
        result = self.queue_array.enqueue(1)
        result &= self.queue_array.enqueue(2)
        result &= self.queue_array.enqueue(3)
        result &= self.queue_array.enqueue(4)
        assert result is True

    def test_array_peek(self) -> None:
        result = self.queue_array.peek()
        assert result == 1

    def test_array_rear(self) -> None:
        result = self.queue_array.rear()
        assert result == 4

    def test_array_dequeue(self) -> None:
        result = self.queue_array.dequeue()
        assert result == 1

    def test_array_is_empty(self) -> None:
        result = self.queue_array.is_empty()
        assert result is False

    def test_array_is_full(self) -> None:
        result = self.queue_array.is_full()
        assert result is False

    def test_array_str(self, array_output: str) -> None:
        result = str(self.queue_array)
        assert result == str(array_output)

    def test_linked_list_enqueue(self) -> None:
        result = self.queue_linked_list.enqueue(1)
        result &= self.queue_linked_list.enqueue(2)
        result &= self.queue_linked_list.enqueue(3)
        result &= self.queue_linked_list.enqueue(4)
        assert result is True

    def test_linked_list_peek(self) -> None:
        result = self.queue_linked_list.peek()
        assert result == 1

    def test_linked_list_rear(self) -> None:
        result = self.queue_linked_list.rear()
        assert result == 4

    def test_linked_list_dequeue(self) -> None:
        result = self.queue_linked_list.dequeue()
        assert result == 1

    def test_linked_list_is_empty(self) -> None:
        result = self.queue_linked_list.is_empty()
        assert result is False

    def test_linked_list_is_full(self) -> None:
        result = self.queue_linked_list.is_full()
        assert result is False

    def test_linked_list_str(self, linked_list_output: str) -> None:
        result = str(self.queue_linked_list)
        assert result == str(linked_list_output)

    def test_array_empty_peek_rear_and_dequeue_return_none(self) -> None:
        q = QueueCircularArray(2)
        assert q.is_empty() is True
        assert q.peek() is None
        assert q.rear() is None
        assert q.dequeue() is None

    def test_array_enqueue_when_full_returns_false(self) -> None:
        q = QueueCircularArray(2)
        assert q.enqueue(1) is True
        assert q.enqueue(2) is True
        assert q.is_full() is True
        assert q.enqueue(3) is False

    def test_array_dequeue_to_empty_then_peek_rear_none(self) -> None:
        q = QueueCircularArray(3)
        for v in (10, 20, 30):
            assert q.enqueue(v) is True
        assert q.dequeue() == 10
        assert q.dequeue() == 20
        assert q.dequeue() == 30
        assert q.is_empty() is True
        # After emptying, internal head/size wrap is covered; now None paths:
        assert q.peek() is None
        assert q.rear() is None

    def test_linked_list_empty_peek_rear_and_dequeue_return_none(self) -> None:
        q = QueueCircularLinkedList(3)
        assert q.is_empty() is True
        assert q.peek() is None
        assert q.rear() is None
        assert q.dequeue() is None

    def test_linked_list_dequeue_last_element_resets_tail(self) -> None:
        q = QueueCircularLinkedList(2)
        assert q.enqueue(7) is True
        assert q.enqueue(8) is True
        assert q.dequeue() == 7
        assert q.dequeue() == 8
        # Validate both pointers reset (exercises lines that only run on last removal)
        assert q.head is None
        assert q.tail is None
        assert q.peek() is None
        assert q.rear() is None

    def test_linked_list_enqueue_when_full_returns_false(self) -> None:
        q = QueueCircularLinkedList(2)
        assert q.enqueue(10) is True
        assert q.enqueue(20) is True
        assert q.is_full() is True
        assert q.enqueue(30) is False
