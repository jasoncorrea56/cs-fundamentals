from __future__ import annotations

import pytest
from automation.resources.data_structures.linked_list_data import (
    DOUBLY_LINKED_LIST_OUTPUT,
)
from cs_fundamentals.data_structures.linked_list_double import DoublyLinkedList, Node


class TestLinkedListDouble:
    """
    Implementation-agnostic test suite.

    Set `ListImpl` in subclasses to point at a different implementation
    (e.g., the Practice variant). All tests use only public methods.
    """

    ListImpl = DoublyLinkedList

    @pytest.fixture()
    def ll(self) -> DoublyLinkedList:
        return self.ListImpl()

    @pytest.fixture()
    def expected_output(self) -> list[int]:
        return DOUBLY_LINKED_LIST_OUTPUT

    # ---------- Original sequence-style tests, rewritten to avoid .head ----------

    def test_add_at_head(self, ll: DoublyLinkedList) -> None:
        ll.add_at_head(1)
        assert ll.get(0) == 1  # Avoid direct .head

    def test_add_at_index(self, ll: DoublyLinkedList, expected_output: list[int]) -> None:
        ll.add_at_head(1)
        ll.add_at_index(1, 2)
        ll.add_at_index(2, 3)
        ll.add_at_index(3, 4)
        ll.add_at_index(4, 5)
        assert ll.get_list() == expected_output

    def test_add_at_tail(self, ll: DoublyLinkedList, expected_output: list[int]) -> None:
        ll.add_at_head(1)
        ll.add_at_index(1, 2)
        ll.add_at_index(2, 3)
        ll.add_at_index(3, 4)
        ll.add_at_index(4, 5)
        ll.add_at_tail(6)
        assert ll.get_list() == expected_output + [6]

    def test_delete_at_index(self, ll: DoublyLinkedList, expected_output: list[int]) -> None:
        # Build 1..6 then delete last
        ll.add_at_head(1)
        for v in [2, 3, 4, 5]:
            ll.add_at_index(v - 1, v)
        ll.add_at_tail(6)
        ll.delete_at_index(5)
        assert ll.get_list() == expected_output

    # ---------- Basics / Edge Cases ----------

    def test_get_node_out_of_range_returns_none_and_get_returns_minus_one(
        self, ll: DoublyLinkedList
    ) -> None:
        ll.add_at_head(10)
        assert ll.get_node(5) is None
        assert ll.get(5) == -1  # Out-of-range

    def test_get_tail_empty_and_singleton(self, ll: DoublyLinkedList) -> None:
        assert ll.get_tail() is None  # Empty list
        ll.add_at_head(1)
        tail = ll.get_tail()
        assert isinstance(tail, Node)
        assert tail.value == 1
        assert tail.next is None

    # ---------- add_at_head variations ----------

    def test_add_at_head_when_non_empty_sets_prev_of_old_head(self, ll: DoublyLinkedList) -> None:
        ll.add_at_head(1)
        ll.add_at_head(2)  # 2 -> 1
        assert ll.get_list() == [2, 1]
        new_head = ll.get_node(0)
        old_head = ll.get_node(1)
        assert new_head is not None and new_head.value == 2
        assert old_head is not None and old_head.value == 1
        # Old head's prev should be the new head
        assert old_head.prev is new_head

    # ---------- add_at_tail variations ----------

    def test_add_at_tail_on_empty_delegates_to_add_at_head(self, ll: DoublyLinkedList) -> None:
        ll.add_at_tail(7)
        assert ll.get_list() == [7]
        n0 = ll.get_node(0)
        assert n0 is not None and n0.prev is None  # Head's prev remains None

    def test_add_at_tail_on_non_empty_sets_prev_link(self, ll: DoublyLinkedList) -> None:
        ll.add_at_head(1)
        ll.add_at_tail(2)
        tail = ll.get_tail()
        assert tail is not None and tail.value == 2
        assert tail.prev is not None and tail.prev.value == 1

    # ---------- add_at_index variations ----------

    def test_add_at_index_zero_routes_to_head(self, ll: DoublyLinkedList) -> None:
        ll.add_at_head(1)
        ll.add_at_index(0, 9)  # Insert at head
        assert ll.get_list() == [9, 1]
        n0 = ll.get_node(0)
        n1 = ll.get_node(1)
        assert n0 is not None and n1 is not None
        assert n1.prev is n0  # Back-link must be updated

    def test_add_at_index_out_of_range_noop(self, ll: DoublyLinkedList) -> None:
        ll.add_at_head(1)
        ll.add_at_index(5, 99)  # No prev node → no-op
        assert ll.get_list() == [1]

    def test_add_at_index_middle_updates_both_links(self, ll: DoublyLinkedList) -> None:
        ll.add_at_head(1)
        ll.add_at_tail(3)
        ll.add_at_index(1, 2)  # Insert between 1 and 3
        assert ll.get_list() == [1, 2, 3]
        mid = ll.get_node(1)
        assert mid is not None and mid.value == 2
        assert mid.prev is not None and mid.prev.value == 1
        assert mid.next is not None and mid.next.value == 3
        # Neighbor back-link updated
        assert mid.next.prev is mid

    def test_add_at_index_tail_case_sets_prev_only(self, ll: DoublyLinkedList) -> None:
        ll.add_at_head(1)
        ll.add_at_index(1, 2)  # Insert at tail position; next_node is None
        tail = ll.get_tail()
        assert tail is not None and tail.value == 2
        assert tail.prev is not None and tail.prev.value == 1

    # ---------- delete_at_index variations ----------

    def test_delete_at_index_out_of_range_noop(self, ll: DoublyLinkedList) -> None:
        ll.add_at_head(1)
        ll.delete_at_index(3)  # Nothing to delete
        assert ll.get_list() == [1]

    def test_delete_at_index_head_moves_head_and_clears_prev(self, ll: DoublyLinkedList) -> None:
        ll.add_at_head(2)
        ll.add_at_head(1)  # 1 -> 2
        ll.delete_at_index(0)
        assert ll.get_list() == [2]
        n0 = ll.get_node(0)
        assert n0 is not None and n0.prev is None  # New head’s prev cleared

    def test_delete_at_index_middle_updates_neighbor_links(self, ll: DoublyLinkedList) -> None:
        for v in [1, 2, 3, 4]:
            if ll.get_node(0) is None:
                ll.add_at_head(v)
            else:
                ll.add_at_tail(v)  # Build 1,2,3,4
        ll.delete_at_index(2)  # Remove value 3
        assert ll.get_list() == [1, 2, 4]
        n1 = ll.get_node(1)
        n2 = ll.get_node(2)
        assert n1 is not None and n2 is not None
        assert n1.next is n2 and n2.prev is n1

    # ---------- get_list duplicate early-stop ----------

    def test_get_list_stops_on_duplicate_value(self, ll: DoublyLinkedList) -> None:
        for v in [1, 2, 3]:
            if ll.get_node(0) is None:
                ll.add_at_head(v)
            else:
                ll.add_at_tail(v)
        # Append a duplicate value at the end; get_list should stop when it encounters 1 again
        ll.add_at_tail(1)
        out = ll.get_list()
        assert out == [1, 2, 3]  # Teaching impls: early-stop at duplicate
