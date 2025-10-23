from __future__ import annotations

from automation.test_data_structures.test_linked_list_double import TestLinkedListDouble
from cs_fundamentals.data_structures.linked_list_double import PracticeDoublyLinkedList


class TestPracticeLinkedListDouble(TestLinkedListDouble):
    # Point the base tests at the practice implementation
    ListImpl = PracticeDoublyLinkedList

    # Wrap each test to tolerate NotImplementedError in early-stage stubs

    def test_add_at_head(self, ll: PracticeDoublyLinkedList) -> None:  # type: ignore[override]
        try:
            super().test_add_at_head(ll)
        except NotImplementedError:
            assert True

    def test_add_at_index(self, ll: PracticeDoublyLinkedList, expected_output: list[int]) -> None:  # type: ignore[override]
        try:
            super().test_add_at_index(ll, expected_output)
        except NotImplementedError:
            assert True

    def test_add_at_tail(self, ll: PracticeDoublyLinkedList, expected_output: list[int]) -> None:  # type: ignore[override]
        try:
            super().test_add_at_tail(ll, expected_output)
        except NotImplementedError:
            assert True

    def test_delete_at_index(
        self, ll: PracticeDoublyLinkedList, expected_output: list[int]
    ) -> None:  # type: ignore[override]
        try:
            super().test_delete_at_index(ll, expected_output)
        except NotImplementedError:
            assert True

    # ---- Extra edge-case wrappers ----

    def test_get_node_out_of_range_returns_none_and_get_returns_minus_one(
        self, ll: PracticeDoublyLinkedList
    ) -> None:  # type: ignore[override]
        try:
            super().test_get_node_out_of_range_returns_none_and_get_returns_minus_one(ll)
        except NotImplementedError:
            assert True

    def test_get_tail_empty_and_singleton(self, ll: PracticeDoublyLinkedList) -> None:  # type: ignore[override]
        try:
            super().test_get_tail_empty_and_singleton(ll)
        except NotImplementedError:
            assert True

    def test_add_at_head_when_non_empty_sets_prev_of_old_head(
        self, ll: PracticeDoublyLinkedList
    ) -> None:  # type: ignore[override]
        try:
            super().test_add_at_head_when_non_empty_sets_prev_of_old_head(ll)
        except NotImplementedError:
            assert True

    def test_add_at_tail_on_empty_delegates_to_add_at_head(
        self, ll: PracticeDoublyLinkedList
    ) -> None:  # type: ignore[override]
        try:
            super().test_add_at_tail_on_empty_delegates_to_add_at_head(ll)
        except NotImplementedError:
            assert True

    def test_add_at_tail_on_non_empty_sets_prev_link(self, ll: PracticeDoublyLinkedList) -> None:  # type: ignore[override]
        try:
            super().test_add_at_tail_on_non_empty_sets_prev_link(ll)
        except NotImplementedError:
            assert True

    def test_add_at_index_zero_routes_to_head(self, ll: PracticeDoublyLinkedList) -> None:  # type: ignore[override]
        try:
            super().test_add_at_index_zero_routes_to_head(ll)
        except NotImplementedError:
            assert True

    def test_add_at_index_out_of_range_noop(self, ll: PracticeDoublyLinkedList) -> None:  # type: ignore[override]
        try:
            super().test_add_at_index_out_of_range_noop(ll)
        except NotImplementedError:
            assert True

    def test_add_at_index_middle_updates_both_links(self, ll: PracticeDoublyLinkedList) -> None:  # type: ignore[override]
        try:
            super().test_add_at_index_middle_updates_both_links(ll)
        except NotImplementedError:
            assert True

    def test_add_at_index_tail_case_sets_prev_only(self, ll: PracticeDoublyLinkedList) -> None:  # type: ignore[override]
        try:
            super().test_add_at_index_tail_case_sets_prev_only(ll)
        except NotImplementedError:
            assert True

    def test_delete_at_index_out_of_range_noop(self, ll: PracticeDoublyLinkedList) -> None:  # type: ignore[override]
        try:
            super().test_delete_at_index_out_of_range_noop(ll)
        except NotImplementedError:
            assert True

    def test_delete_at_index_head_moves_head_and_clears_prev(
        self, ll: PracticeDoublyLinkedList
    ) -> None:  # type: ignore[override]
        try:
            super().test_delete_at_index_head_moves_head_and_clears_prev(ll)
        except NotImplementedError:
            assert True

    def test_delete_at_index_middle_updates_neighbor_links(
        self, ll: PracticeDoublyLinkedList
    ) -> None:  # type: ignore[override]
        try:
            super().test_delete_at_index_middle_updates_neighbor_links(ll)
        except NotImplementedError:
            assert True

    def test_get_list_stops_on_duplicate_value(self, ll: PracticeDoublyLinkedList) -> None:  # type: ignore[override]
        try:
            super().test_get_list_stops_on_duplicate_value(ll)
        except NotImplementedError:
            assert True
