import pytest
from automation.test_data_structures.test_queue import TestQueue
from data_structures.queue import PracticeQueueCircularArray, PracticeQueueCircularLinkedList


class TestPracticeQueue(TestQueue):

    @classmethod
    def setup_class(cls) -> None:
        cls.queue_array = PracticeQueueCircularArray(4)
        cls.queue_linked_list = PracticeQueueCircularLinkedList(4)

    def test_array_enqueue(self):
        try:
            super().test_array_enqueue()
        except NotImplementedError:
            assert True

    def test_array_peek(self):
        try:
            super().test_array_peek()
        except NotImplementedError:
            assert True

    def test_array_rear(self):
        try:
            super().test_array_rear()
        except NotImplementedError:
            assert True

    def test_array_dequeue(self):
        try:
            super().test_array_dequeue()
        except NotImplementedError:
            assert True

    def test_array_is_empty(self):
        try:
            super().test_array_is_empty()
        except NotImplementedError:
            assert True

    def test_array_is_full(self):
        try:
            super().test_array_is_full()
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("array_output")
    def test_array_str(self, array_output):
        try:
            super().test_array_str(array_output)
        except NotImplementedError:
            assert True

    def test_linked_list_enqueue(self):
        try:
            super().test_linked_list_enqueue()
        except NotImplementedError:
            assert True

    def test_linked_list_peek(self):
        try:
            super().test_linked_list_peek()
        except NotImplementedError:
            assert True

    def test_linked_list_rear(self):
        try:
            super().test_linked_list_rear()
        except NotImplementedError:
            assert True

    def test_linked_list_dequeue(self):
        try:
            super().test_linked_list_dequeue()
        except NotImplementedError:
            assert True

    def test_linked_list_is_empty(self):
        try:
            super().test_linked_list_is_empty()
        except NotImplementedError:
            assert True

    def test_linked_list_is_full(self):
        try:
            super().test_linked_list_is_full()
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("linked_list_output")
    def test_linked_list_str(self, linked_list_output):
        try:
            super().test_linked_list_str(linked_list_output)
        except NotImplementedError:
            assert True
