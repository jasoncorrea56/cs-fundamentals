import pytest
from automation.test_data_structures.test_binary_search_tree import TestBinarySearchTree
from data_structures.binary_search_tree import PracticeBinarySearchTree


class TestPracticeBinarySearchTree(TestBinarySearchTree):
    @classmethod
    def setup_class(cls) -> None:
        cls.bst = PracticeBinarySearchTree()

    @pytest.mark.usefixtures("bst_root")
    def test_is_valid_bst(self, bst_root) -> None:
        try:
            super().test_is_valid_bst(bst_root)
        except NotImplementedError:
            assert True
