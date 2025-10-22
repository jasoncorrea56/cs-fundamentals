from __future__ import annotations

from automation.test_data_structures.test_heap import TestHeap
from cs_fundamentals.data_structures.maxheap import PracticeMaxHeap
from cs_fundamentals.data_structures.minheap import PracticeMinHeap


class TestPracticeHeap(TestHeap):
    @classmethod
    def setup_class(cls) -> None:
        cls.minheap = PracticeMinHeap(4)
        cls.maxheap = PracticeMaxHeap(4)

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

    # ---------- Optional: Practice stub checks (uncomment if you want explicit coverage) ----------
    # def test_practice_minheap_ctor_and_methods_raise_not_implemented(self) -> None:
    #     pmh: PracticeMinHeap = PracticeMinHeap(4)
    #     for call in (lambda: pmh.add(1), pmh.pop, pmh.peek, pmh.size, lambda: str(pmh)):
    #         with pytest.raises(NotImplementedError):
    #             call()
