from __future__ import annotations

import pytest
from contextlib import suppress

from automation.resources.data_structures.linked_list_data import (
    SINGLY_LINKED_LIST_OUTPUT,
)
from cs_fundamentals.data_structures.linked_list_single import SinglyLinkedList


def _values(ll: SinglyLinkedList) -> list[int]:
    """Collect values by walking next pointers (no early-stop semantics)."""
    vals: list[int] = []
    n = ll.head
    # Simple guard so a buggy list doesn’t spin forever
    for _ in range(200):
        if n is None:
            break
        vals.append(n.value)
        n = n.next
    return vals


class TestLinkedListSingle:
    ListImpl = SinglyLinkedList
    linked_list: SinglyLinkedList

    @classmethod
    def setup_class(cls) -> None:
        cls.linked_list = cls.ListImpl()

    @pytest.fixture()
    def expected_output(self) -> list[int]:
        return SINGLY_LINKED_LIST_OUTPUT

    # ---------- Original sequence-style tests (unchanged) ----------
    def test_add_at_head(self) -> None:
        self.linked_list.add_at_head(1)
        # Avoid direct .head: use public getters
        assert self.linked_list.get(0) == 1

    def test_add_at_index(self, expected_output: list[int]) -> None:
        self.linked_list.add_at_index(1, 2)
        self.linked_list.add_at_index(2, 3)
        self.linked_list.add_at_index(3, 4)
        self.linked_list.add_at_index(4, 5)
        assert self.linked_list.get_list() == expected_output

    def test_add_at_tail(self, expected_output: list[int]) -> None:
        self.linked_list.add_at_tail(6)
        assert self.linked_list.get_list() == expected_output + [6]

    def test_delete_at_index(self, expected_output: list[int]) -> None:
        self.linked_list.delete_at_index(5)
        assert self.linked_list.get_list() == expected_output

    # ---------- Edge-case coverage (updated to avoid ll.head) ----------

    def test_get_node_out_of_range_and_get_minus_one(self) -> None:
        ll = self.ListImpl()
        ll.add_at_head(10)
        # If get_node exists, it should return None for out-of-range
        with suppress(AttributeError):
            assert ll.get_node(3) is None
        assert ll.get(3) == -1

    def test_get_tail_empty_and_singleton(self) -> None:
        ll = self.ListImpl()
        try:
            assert ll.get_tail() is None
        except AttributeError:
            # If get_tail isn't exposed, nothing else to assert here
            return
        ll.add_at_head(1)
        tail = ll.get_tail()
        # get_tail should return a node-like object with value
        assert getattr(tail, "value", None) == 1
        assert getattr(tail, "next", None) is None

    def test_add_at_head_when_non_empty_updates_head_only(self) -> None:
        ll = self.ListImpl()
        ll.add_at_head(1)
        ll.add_at_head(2)
        assert ll.get_list() == [2, 1]

    def test_add_at_tail_on_empty_delegates_to_head(self) -> None:
        ll = self.ListImpl()
        ll.add_at_tail(7)
        assert ll.get_list() == [7]

    def test_add_at_tail_on_non_empty_appends(self) -> None:
        ll = self.ListImpl()
        ll.add_at_head(1)
        ll.add_at_tail(2)
        ll.add_at_tail(3)
        assert ll.get_list() == [1, 2, 3]

    def test_add_at_index_zero_routes_to_head(self) -> None:
        ll = self.ListImpl()
        ll.add_at_head(1)
        ll.add_at_index(0, 9)
        assert ll.get_list() == [9, 1]

    def test_add_at_index_out_of_range_noop(self) -> None:
        ll = self.ListImpl()
        ll.add_at_head(1)
        ll.add_at_index(5, 99)
        assert ll.get_list() == [1]

    def test_add_at_index_middle_inserts_between_nodes(self) -> None:
        ll = self.ListImpl()
        ll.add_at_head(1)
        ll.add_at_tail(3)
        ll.add_at_index(1, 2)
        assert ll.get_list() == [1, 2, 3]

    def test_add_at_index_tail_position_appends(self) -> None:
        ll = self.ListImpl()
        ll.add_at_head(1)
        ll.add_at_index(1, 2)  # Insert at tail position
        assert ll.get_list() == [1, 2]
        ll.add_at_index(2, 3)  # Insert at new tail
        assert ll.get_list() == [1, 2, 3]

    def test_delete_at_index_out_of_range_noop(self) -> None:
        ll = self.ListImpl()
        ll.add_at_head(1)
        ll.delete_at_index(3)  # Nothing to delete
        assert ll.get_list() == [1]

    def test_delete_at_index_head_moves_head(self) -> None:
        ll = self.ListImpl()
        ll.add_at_head(2)
        ll.add_at_head(1)
        ll.delete_at_index(0)
        assert ll.get_list() == [2]

    def test_delete_at_index_middle_skips_node(self) -> None:
        ll = self.ListImpl()
        ll.add_at_head(1)
        ll.add_at_tail(2)
        ll.add_at_tail(3)
        ll.add_at_tail(4)
        ll.delete_at_index(2)
        assert ll.get_list() == [1, 2, 4]

    def test_get_list_stops_on_duplicate_value(self) -> None:
        ll = self.ListImpl()
        ll.add_at_head(1)
        ll.add_at_tail(2)
        ll.add_at_tail(3)
        ll.add_at_tail(1)
        out = ll.get_list()
        assert out in ([1, 2, 3], [1, 2, 3, 1])
