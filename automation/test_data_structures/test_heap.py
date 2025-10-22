from __future__ import annotations

import sys

from automation.resources.data_structures.heap_data import (
    MAXHEAP_OUTPUT,
    MINHEAP_OUTPUT,
)
from cs_fundamentals.data_structures.maxheap import MaxHeap
from cs_fundamentals.data_structures.minheap import MinHeap


class TestHeap:
    @classmethod
    def setup_class(cls) -> None:
        cls.minheap = MinHeap(4)
        cls.maxheap = MaxHeap(4)

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
        contents: list[int] = eval(s, {"__builtins__": {}})  # safe here
        assert len(contents) == 3
        assert min(contents) == 1

    # ---------- MaxHeap core tests ----------

    def test_maxheap_add(self) -> None:
        result = self.maxheap.add(1)
        result &= self.maxheap.add(2)
        result &= self.maxheap.add(3)
        result &= self.maxheap.add(4)
        assert result is True

    def test_maxheap_pop(self) -> None:
        result = self.maxheap.pop()
        assert result == 4

    def test_maxheap_peek(self) -> None:
        result = self.maxheap.peek()
        assert result == 3

    def test_maxheap_size(self) -> None:
        result = self.maxheap.size()
        assert result == 3

    def test_maxheap_str(self) -> None:
        result = self.maxheap.__str__()
        assert result == MAXHEAP_OUTPUT

    # ---------- MaxHeap additional edge/behavior tests ----------

    def test_add_overflow_returns_false_and_does_not_grow(self) -> None:
        """Fill heap then trigger overflow branch (prints + False)."""
        h: MaxHeap = MaxHeap(2)
        assert h.add(10) is True
        assert h.add(20) is True
        assert h.add(25) is False  # overflow
        assert h.size() == 2
        assert h.peek() == 20  # max at root

    def test_add_larger_bubbles_up(self) -> None:
        """Adding a larger element should bubble to root via swap loop."""
        h: MaxHeap = MaxHeap(10)
        assert h.add(5) is True
        assert h.add(8) is True
        assert h.add(3) is True
        assert h.add(12) is True  # should bubble to root
        assert h.peek() == 12
        assert h.pop() == 12
        assert h.peek() == 8

    def test_pop_from_empty_returns_neg_sys_maxsize(self) -> None:
        """Empty pop takes guarded early return."""
        h: MaxHeap = MaxHeap(3)
        assert h.size() == 0
        assert h.pop() == -sys.maxsize
        assert h.size() == 0

    def test_pop_with_only_left_child_exercises_no_right_branch(self) -> None:
        """
        Two items -> only a left child exists; hits 'no right child' path.
        """
        h: MaxHeap = MaxHeap(3)
        assert h.add(7) is True
        assert h.add(5) is True  # heap [7, 5]
        assert h.pop() == 7
        assert h.size() == 1
        assert h.peek() == 5

    def test_peek_on_empty_returns_neg_sys_maxsize(self) -> None:
        """Empty peek returns -sys.maxsize."""
        h: MaxHeap = MaxHeap(1)
        assert h.peek() == -sys.maxsize

    def test_str_representation_slices_active_region_only(self) -> None:
        """__str__ should include only active heap contents."""
        h: MaxHeap = MaxHeap(5)
        for v in (2, 10, 6):
            assert h.add(v) is True
        s: str = str(h)
        assert s.startswith("[") and s.endswith("]")
        contents = eval(s, {"__builtins__": {}})
        assert len(contents) == 3
        assert max(contents) == 10
