from __future__ import annotations

import sys
from ast import literal_eval

from automation.resources.data_structures.heap_data import MINHEAP_OUTPUT
from cs_fundamentals.data_structures.min_heap import MinHeap


class TestHeap:
    @classmethod
    def setup_class(cls) -> None:
        cls.minheap = MinHeap(4)

    # ---------- MinHeap core tests ----------

    def test_minheap_add(self) -> None:
        result = self.minheap.add(1)
        result &= self.minheap.add(2)
        result &= self.minheap.add(3)
        result &= self.minheap.add(4)
        assert result is True

    def test_minheap_pop(self) -> None:
        result = self.minheap.pop()
        assert result == 1

    def test_minheap_peek(self) -> None:
        result = self.minheap.peek()
        assert result == 2

    def test_minheap_size(self) -> None:
        result = self.minheap.size()
        assert result == 3

    def test_minheap_str(self) -> None:
        result = self.minheap.__str__()
        assert result == MINHEAP_OUTPUT

    # ---------- MinHeap additional edge/behavior tests ----------

    def test_min_add_overflow_returns_false_and_does_not_grow(self) -> None:
        """Fill heap then exercise overflow branch (prints + False)."""
        h: MinHeap = MinHeap(2)
        assert h.add(10) is True
        assert h.add(20) is True
        assert h.add(5) is False  # overflow
        assert h.size() == 2  # unchanged
        assert h.peek() == 10  # existing min intact

    def test_min_add_smaller_bubbles_up(self) -> None:
        """Adding a smaller element should bubble to root via swap loop."""
        h: MinHeap = MinHeap(10)
        assert h.add(10) is True
        assert h.add(7) is True
        assert h.add(12) is True
        assert h.add(5) is True  # should bubble above 10
        assert h.peek() == 5
        assert h.pop() == 5
        assert h.peek() == 7

    def test_min_pop_from_empty_returns_sys_maxsize(self) -> None:
        """Empty pop takes guarded early return."""
        h: MinHeap = MinHeap(3)
        assert h.size() == 0
        assert h.pop() == sys.maxsize
        assert h.size() == 0

    def test_min_pop_with_only_left_child_exercises_no_right_branch(self) -> None:
        """
        Two items -> only a left child exists; hits 'no right child' path.
        """
        h: MinHeap = MinHeap(3)
        assert h.add(4) is True
        assert h.add(9) is True  # heap [4, 9]
        assert h.pop() == 4
        assert h.size() == 1
        assert h.peek() == 9

    def test_min_peek_on_empty_returns_sys_maxsize(self) -> None:
        """Empty peek returns sys.maxsize."""
        h: MinHeap = MinHeap(1)
        assert h.peek() == sys.maxsize

    def test_min_str_representation_slices_active_region_only(self) -> None:
        """__str__ should include only active heap contents."""
        h: MinHeap = MinHeap(5)
        for v in (3, 8, 1):
            assert h.add(v) is True
        _ = h.peek()  # ensure heap property
        s: str = str(h)
        assert s.startswith("[") and s.endswith("]")
        contents = literal_eval(s)
        assert len(contents) == 3
        assert min(contents) == 1
