from automation.test_data_structures.test_heap import TestHeap
from cs_fundamentals.data_structures.maxheap import PracticeMaxHeap
from cs_fundamentals.data_structures.minheap import PracticeMinHeap


class TestPracticeHeap(TestHeap):
    @classmethod
    def setup_class(cls) -> None:
        cls.minheap = PracticeMinHeap(4)
        cls.maxheap = PracticeMaxHeap(4)

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
