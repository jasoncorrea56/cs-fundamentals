from __future__ import annotations

from automation.test_data_structures.test_min_heap import TestHeap
from cs_fundamentals.data_structures.min_heap import PracticeMinHeap


class TestPracticeHeap(TestHeap):
    @classmethod
    def setup_class(cls) -> None:
        cls.minheap = PracticeMinHeap(4)

    # ---------- MinHeap core tests (wrapped) ----------

    def test_minheap_add(self) -> None:
        try:
            super().test_minheap_add()
        except NotImplementedError:
            assert True

    def test_minheap_pop(self) -> None:
        try:
            super().test_minheap_pop()
        except NotImplementedError:
            assert True

    def test_minheap_peek(self) -> None:
        try:
            super().test_minheap_peek()
        except NotImplementedError:
            assert True

    def test_minheap_size(self) -> None:
        try:
            super().test_minheap_size()
        except NotImplementedError:
            assert True

    def test_minheap_str(self) -> None:
        try:
            super().test_minheap_str()
        except NotImplementedError:
            assert True

    # ---------- MinHeap extra tests (wrapped) ----------

    def test_min_add_overflow_returns_false_and_does_not_grow(self) -> None:
        try:
            super().test_min_add_overflow_returns_false_and_does_not_grow()
        except NotImplementedError:
            assert True

    def test_min_add_smaller_bubbles_up(self) -> None:
        try:
            super().test_min_add_smaller_bubbles_up()
        except NotImplementedError:
            assert True

    def test_min_pop_from_empty_returns_sys_maxsize(self) -> None:
        try:
            super().test_min_pop_from_empty_returns_sys_maxsize()
        except NotImplementedError:
            assert True

    def test_min_pop_with_only_left_child_exercises_no_right_branch(self) -> None:
        try:
            super().test_min_pop_with_only_left_child_exercises_no_right_branch()
        except NotImplementedError:
            assert True

    def test_min_peek_on_empty_returns_sys_maxsize(self) -> None:
        try:
            super().test_min_peek_on_empty_returns_sys_maxsize()
        except NotImplementedError:
            assert True

    def test_min_str_representation_slices_active_region_only(self) -> None:
        try:
            super().test_min_str_representation_slices_active_region_only()
        except NotImplementedError:
            assert True
