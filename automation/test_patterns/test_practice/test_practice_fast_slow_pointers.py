import pytest
from automation.test_patterns.test_fast_slow_pointers import TestFastSlowPointers
from cs_fundamentals.data_structures.linked_list_single import Node, SinglyLinkedList
from cs_fundamentals.patterns.fast_slow_pointers import PracticeFastSlowPointers


class TestPracticeFastSlowPointers(TestFastSlowPointers):
    @classmethod
    def setup_class(cls) -> None:
        cls.fs_pointers = PracticeFastSlowPointers()
        cls.linked_list = SinglyLinkedList()

    def test_build_linked_list_cycle(self) -> None:
        try:
            super().test_build_linked_list_cycle()
        except NotImplementedError:
            assert True

    def test_has_cycle_in_linked_list(self) -> None:
        try:
            super().test_has_cycle_in_linked_list()
        except NotImplementedError:
            assert True

    @pytest.mark.usefixtures("cycle_first_node")
    def test_get_first_node_for_cycle_in_linked_list(self, cycle_first_node: Node) -> None:
        try:
            super().test_get_first_node_for_cycle_in_linked_list(cycle_first_node)
        except NotImplementedError:
            assert True
