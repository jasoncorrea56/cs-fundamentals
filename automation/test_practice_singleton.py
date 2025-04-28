from automation.test_singleton import TestSingletonPattern
from singleton import (
    PracticeSingletonClass,
    PracticeSingletonChild,
    PracticeBorgSingletonClass,
    PracticeBorgSingletonChild,
    PracticeBorgSingletonResetChild,
)


class TestPracticeSingletonPattern(TestSingletonPattern):
    @classmethod
    def setup_class(cls) -> None:
        pass

    def test_singleton(self):
        try:
            singleton = PracticeSingletonClass()
            singleton2 = PracticeSingletonClass()
            singleton.singleton_variable = False
            assert singleton is singleton2
            assert hasattr(singleton2, "singleton_variable")
        except NotImplementedError:
            assert True

    def test_singleton_inheritance(self):
        try:
            singleton = PracticeSingletonClass()
            singleton_child = PracticeSingletonChild()
            singleton.singleton_inheritance_variable = False
            assert singleton_child is singleton
            assert hasattr(singleton_child, "singleton_inheritance_variable")
        except NotImplementedError:
            assert True

    def test_borg_singleton(self):
        try:
            borg = PracticeBorgSingletonClass()
            borg_child = PracticeBorgSingletonChild()
            borg.shared_variable = False
            assert borg_child is not borg
            assert hasattr(borg_child, "shared_variable")
        except NotImplementedError:
            assert True

    def test_borg_singleton_shared_state_reset(self):
        try:
            borg = PracticeBorgSingletonClass()
            borg.shared_variable = False
            borg_reset_child = PracticeBorgSingletonResetChild()
            assert borg_reset_child is not borg
            assert not hasattr(borg_reset_child, "shared_variable")
        except NotImplementedError:
            assert True
