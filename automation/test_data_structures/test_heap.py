from automation.resources.data_structures.heap_data import (
    MAXHEAP_OUTPUT,
    MINHEAP_OUTPUT,
)
from data_structures.heap import MaxHeap, MinHeap


class TestHeap(object):
    @classmethod
    def setup_class(cls) -> None:
        cls.minheap = MinHeap(4)
        cls.maxheap = MaxHeap(4)

    def test_minheap_add(self):
        result = self.minheap.add(1)
        result &= self.minheap.add(2)
        result &= self.minheap.add(3)
        result &= self.minheap.add(4)
        assert result is True

    def test_minheap_pop(self):
        result = self.minheap.pop()
        assert result == 1

    def test_minheap_peek(self):
        result = self.minheap.peek()
        assert result == 2

    def test_minheap_size(self):
        result = self.minheap.size()
        assert result == 3

    def test_minheap_str(self):
        result = self.minheap.__str__()
        assert result == MINHEAP_OUTPUT

    def test_maxheap_add(self):
        result = self.maxheap.add(1)
        result &= self.maxheap.add(2)
        result &= self.maxheap.add(3)
        result &= self.maxheap.add(4)
        assert result is True

    def test_maxheap_pop(self):
        result = self.maxheap.pop()
        assert result == 4

    def test_maxheap_peek(self):
        result = self.maxheap.peek()
        assert result == 3

    def test_maxheap_size(self):
        result = self.maxheap.size()
        assert result == 3

    def test_maxheap_str(self):
        result = self.maxheap.__str__()
        assert result == MAXHEAP_OUTPUT
