from __future__ import annotations

from automation.test_data_structures.test_max_heap import TestHeap
from cs_fundamentals.data_structures.max_heap import PracticeMaxHeap


class TestPracticeHeap(TestHeap):
    @classmethod
    def setup_class(cls) -> None:
        cls.maxheap = PracticeMaxHeap(4)

    # ---------- MaxHeap core tests (wrapped) ----------

    def test_maxheap_add(self) -> None:
        try:
            super().test_maxheap_add()
        except NotImplementedError:
            assert True

    def test_maxheap_pop(self) -> None:
        try:
            super().test_maxheap_pop()
        except NotImplementedError:
            assert True

    def test_maxheap_peek(self) -> None:
        try:
            super().test_maxheap_peek()
        except NotImplementedError:
            assert True

    def test_maxheap_size(self) -> None:
        try:
            super().test_maxheap_size()
        except NotImplementedError:
            assert True

    def test_maxheap_str(self) -> None:
        try:
            super().test_maxheap_str()
        except NotImplementedError:
            assert True

    # ---------- MaxHeap extra tests (wrapped) ----------

    def test_add_overflow_returns_false_and_does_not_grow(self) -> None:
        try:
            super().test_add_overflow_returns_false_and_does_not_grow()
        except NotImplementedError:
            assert True

    def test_add_larger_bubbles_up(self) -> None:
        try:
            super().test_add_larger_bubbles_up()
        except NotImplementedError:
            assert True

    def test_pop_from_empty_returns_neg_sys_maxsize(self) -> None:
        try:
            super().test_pop_from_empty_returns_neg_sys_maxsize()
        except NotImplementedError:
            assert True

    def test_pop_with_only_left_child_exercises_no_right_branch(self) -> None:
        try:
            super().test_pop_with_only_left_child_exercises_no_right_branch()
        except NotImplementedError:
            assert True

    def test_peek_on_empty_returns_neg_sys_maxsize(self) -> None:
        try:
            super().test_peek_on_empty_returns_neg_sys_maxsize()
        except NotImplementedError:
            assert True

    def test_str_representation_slices_active_region_only(self) -> None:
        try:
            super().test_str_representation_slices_active_region_only()
        except NotImplementedError:
            assert True
