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
