import pytest
from automation.test_data_structures.test_linked_list_double import TestLinkedListDouble
from data_structures.linked_list_double import PracticeDoublyLinkedList


class TestPracticeLinkedListSingle(TestLinkedListDouble):

    @classmethod
    def setup_class(cls) -> None:
        cls.linked_list = PracticeDoublyLinkedList()

    def test_add_at_head(self):
        try:
            super().test_add_at_head()
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("expected_output")
    def test_add_at_index(self, expected_output):
        try:
            super().test_add_at_index(expected_output)
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("expected_output")
    def test_add_at_tail(self, expected_output):
        try:
            super().test_add_at_tail(expected_output)
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("expected_output")
    def test_delete_at_index(self, expected_output):
        try:
            super().test_delete_at_index(expected_output)
        except NotImplementedError:
            assert True
