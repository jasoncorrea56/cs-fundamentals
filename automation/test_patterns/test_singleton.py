from cs_fundamentals.patterns.singleton import (
    NormalClass,
    NormalChild,
    SingletonClass,
    SingletonChild,
    BorgSingletonClass,
    BorgSingletonChild,
    BorgSingletonResetChild,
)


class TestSingletonPattern:
    @classmethod
    def setup_class(cls) -> None:
        pass

    def test_singleton(self) -> None:
        singleton = SingletonClass()
        singleton2 = SingletonClass()
        singleton.singleton_variable = False
        assert singleton is singleton2
        assert hasattr(singleton2, "singleton_variable")

    def test_singleton_inheritance(self) -> None:
        singleton = SingletonClass()
        singleton_child = SingletonChild()
        singleton.singleton_inheritance_variable = False
        assert singleton_child is singleton
        assert hasattr(singleton_child, "singleton_inheritance_variable")

    def test_borg_singleton(self) -> None:
        borg = BorgSingletonClass()
        borg_child = BorgSingletonChild()
        borg.shared_variable = False
        assert borg_child is not borg
        assert hasattr(borg_child, "shared_variable")

    def test_borg_singleton_shared_state_reset(self) -> None:
        borg = BorgSingletonClass()
        borg.shared_variable = False
        borg_reset_child = BorgSingletonResetChild()
        assert borg_reset_child is not borg
        assert not hasattr(borg_reset_child, "shared_variable")

    def test_normal_base_print(self, capsys) -> None:
        """Covers NormalClass.print_access (line ~27)."""
        base = NormalClass()
        base.print_access()
        out = capsys.readouterr().out
        assert "Printed NormalClass" in out

    def test_normal_class_access_and_print(self, capsys) -> None:
        # Hit NormalClass.__init__, set_access, getters, and NormalChild.print_access
        base = NormalClass()
        child = NormalChild()

        base.set_access("Normalized")
        assert base.get_class_access() == "Normalized"
        assert base.get_instance_access() == "Normalized"

        # Child inherits getters; class var is defined on NormalClass so child sees it
        assert child.get_class_access() == "Normalized"
        # Child has its own instance var (still None)
        assert child.get_instance_access() is None

        child.print_access()
        out = capsys.readouterr().out
        assert "Normal class_access = Normalized" in out
        assert "Normal instance_access = None" in out

    def test_singleton_accessors_and_print(self, capsys) -> None:
        # Create the child first so the one shared instance is a SingletonChild
        child = SingletonChild()
        root = SingletonClass()

        assert child is root

        child.set_access("Singletoned")
        assert child.get_class_access() == "Singletoned"
        assert child.get_instance_access() == "Singletoned"

        child.print_access()
        out = capsys.readouterr().out
        assert "Singleton class_access = Singletoned" in out
        assert "Singleton instance_access = Singletoned" in out

    def test_singleton_child_print_force_child_instance(self, capsys) -> None:
        # Ensure coverage of SingletonChild.print_access by making the first
        # singleton instance come from the child class. Restore afterwards.
        orig = SingletonClass._instance
        try:
            SingletonClass._instance = None  # Reset the shared instance
            child = SingletonChild()  # First creation > instance is child-typed
            child.set_access("CoverMe")
            child.print_access()
            out = capsys.readouterr().out
            assert "Singleton class_access = CoverMe" in out
            assert "Singleton instance_access = CoverMe" in out
        finally:
            SingletonClass._instance = orig  # Restore for other tests

    def test_borg_accessors_and_print(self, capsys) -> None:
        # Exercise Borg set/get across multiple instances and print_access
        a = BorgSingletonChild()
        b = BorgSingletonChild()

        a.set_access("Borged")
        assert a.get_class_access() == "Borged"
        assert a.get_instance_access() == "Borged"

        # Shared monostate: b sees the same instance/class values through shared dict
        assert b.get_instance_access() == "Borged"
        assert b.get_class_access() == "Borged"

        b.print_access()
        out = capsys.readouterr().out
        assert "BorgSingleton class_access = Borged" in out
        assert "BorgSingleton instance_access = Borged" in out

    def test_borg_reset_child_has_fresh_state(self) -> None:
        # Ensure Reset subclass does not share prior monostate contents
        _ = BorgSingletonChild().set_access("SharedBeforeReset")
        reset = BorgSingletonResetChild()
        # Fresh dict for this subclass => no prior instance value
        assert reset.get_instance_access() is None

    def test_borg_reset_child_print(self, capsys) -> None:
        """Covers BorgSingletonResetChild.print_access (lines ~118–119)."""
        reset = BorgSingletonResetChild()
        reset.set_access("Fresh")
        reset.print_access()
        out = capsys.readouterr().out
        assert "BorgSingleton class_access = Fresh" in out
        assert "BorgSingleton instance_access = Fresh" in out
