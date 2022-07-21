import pytest
from automation.test_data_structures.test_stack import TestStack
from data_structures.stack import PracticeStackArray, PracticeStackLinkedList


class TestPracticeStack(TestStack):

    @classmethod
    def setup_class(cls) -> None:
        cls.stack_array = PracticeStackArray()
        cls.stack_linked_list = PracticeStackLinkedList()

    def test_array_push(self):
        try:
            super().test_array_push()
        except NotImplementedError:
            assert True

    def test_array_peek(self):
        try:
            super().test_array_peek()
        except NotImplementedError:
            assert True

    def test_array_pop(self):
        try:
            super().test_array_pop()
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("expected_output")
    def test_array_str(self, expected_output):
        try:
            super().test_array_str(expected_output)
        except NotImplementedError:
            assert True

    def test_linked_list_push(self):
        try:
            super().test_linked_list_push()
        except NotImplementedError:
            assert True

    def test_linked_list_peek(self):
        try:
            super().test_linked_list_peek()
        except NotImplementedError:
            assert True

    def test_linked_list_pop(self):
        try:
            super().test_linked_list_pop()
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("expected_output")
    def test_linked_list_str(self, expected_output):
        try:
            super().test_linked_list_str(expected_output)
        except NotImplementedError:
            assert True
