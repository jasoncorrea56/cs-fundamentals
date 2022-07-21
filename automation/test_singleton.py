import pytest
from singleton import SingletonClass, SingletonChild, BorgSingletonClass, BorgSingletonChild, BorgSingletonResetChild


class TestSingletonPattern(object):

    @classmethod
    def setup_class(cls) -> None:
        pass

    def test_singleton(self):
        singleton = SingletonClass()
        singleton2 = SingletonClass()
        singleton.singleton_variable = False
        assert singleton is singleton2
        assert hasattr(singleton2, "singleton_variable")

    def test_singleton_inheritance(self):
        singleton = SingletonClass()
        singleton_child = SingletonChild()
        singleton.singleton_inheritance_variable = False
        assert singleton_child is singleton
        assert hasattr(singleton_child, "singleton_inheritance_variable")

    def test_borg_singleton(self):
        borg = BorgSingletonClass()
        borg_child = BorgSingletonChild()
        borg.shared_variable = False
        assert borg_child is not borg
        assert hasattr(borg_child, "shared_variable")

    def test_borg_singleton_shared_state_reset(self):
        borg = BorgSingletonClass()
        borg.shared_variable = False
        borg_reset_child = BorgSingletonResetChild()
        assert borg_reset_child is not borg
        assert not hasattr(borg_reset_child, "shared_variable")
