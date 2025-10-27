from __future__ import annotations

from typing import Any, ClassVar, TypeVar


# ---------- Normal class (non-singleton) ----------


class NormalClass:
    __class_var: ClassVar[str | None] = None

    def __init__(self) -> None:
        self.__instance_var: str | None = None

    def set_access(self, value: str) -> None:
        # Assign class variable via the class (not the instance)
        type(self).__class_var = value
        self.__instance_var = value

    def get_class_access(self) -> str | None:
        return self.__class_var

    def get_instance_access(self) -> str | None:
        return self.__instance_var

    def print_access(self) -> None:
        print("Printed NormalClass")


class NormalChild(NormalClass):
    def print_access(self) -> None:
        print(f"Normal class_access = {self.get_class_access()}")
        print(f"Normal instance_access = {self.get_instance_access()}")


# ---------- Classic Singleton ----------

_SelfSingleton = TypeVar("_SelfSingleton", bound="SingletonClass")


class SingletonClass:
    __class_var: ClassVar[str | None] = None
    _instance: ClassVar[SingletonClass | None] = None

    def __new__(cls: type[_SelfSingleton]) -> _SelfSingleton:
        # Always use the base-class slot so the entire hierarchy shares one instance
        if SingletonClass._instance is None:
            # The first class to construct decides the concrete type (cls)
            SingletonClass._instance = super().__new__(cls)
        return SingletonClass._instance  # type: ignore[return-value]

    def __init__(self) -> None:
        self.__instance_var: str | None = None

    def set_access(self, value: str) -> None:
        type(self).__class_var = value
        self.__instance_var = value

    def get_class_access(self) -> str | None:
        return self.__class_var

    def get_instance_access(self) -> str | None:
        return self.__instance_var

    def print_access(self) -> None:
        print(f"Singleton class_access = {self.get_class_access()}")
        print(f"Singleton instance_access = {self.get_instance_access()}")


class SingletonChild(SingletonClass):
    def print_access(self) -> None:
        print(f"Singleton class_access = {self.get_class_access()}")
        print(f"Singleton instance_access = {self.get_instance_access()}")


# ---------- Borg (Monostate) Singleton ----------

_SelfBorg = TypeVar("_SelfBorg", bound="BorgSingletonClass")


class BorgSingletonClass:
    _shared_borg_state: ClassVar[dict[str, Any]] = {}
    __class_var: ClassVar[str | None] = None

    def __new__(cls: type[_SelfBorg], *args: Any, **kwargs: Any) -> _SelfBorg:
        obj = super().__new__(cls)
        # Share state among *all* instances of this class hierarchy
        obj.__dict__ = cls._shared_borg_state
        return obj

    def __init__(self) -> None:
        self.__instance_var: str | None = None

    def set_access(self, value: str) -> None:
        type(self).__class_var = value
        self.__instance_var = value

    def get_class_access(self) -> str | None:
        return self.__class_var

    def get_instance_access(self) -> str | None:
        return self.__instance_var

    # def print_access(self) -> None:
    #     print("Printed BorgSingletonClass")


class BorgSingletonChild(BorgSingletonClass):
    def print_access(self) -> None:
        print(f"BorgSingleton class_access = {self.get_class_access()}")
        print(f"BorgSingleton instance_access = {self.get_instance_access()}")


class BorgSingletonResetChild(BorgSingletonClass):
    # Fresh shared state for this subclass
    _shared_borg_state: ClassVar[dict[str, Any]] = {}

    def print_access(self) -> None:
        print(f"BorgSingleton class_access = {self.get_class_access()}")
        print(f"BorgSingleton instance_access = {self.get_instance_access()}")


# ---------- Practice stubs ----------


class PracticeSingletonClass:
    def __new__(cls: type[PracticeSingletonClass]) -> PracticeSingletonClass:
        raise NotImplementedError  # pragma: no cover


class PracticeSingletonChild(PracticeSingletonClass):
    def print_access(self) -> None:
        raise NotImplementedError  # pragma: no cover


class PracticeBorgSingletonClass:
    def __new__(
        cls: type[PracticeBorgSingletonClass], *args: Any, **kwargs: Any
    ) -> PracticeBorgSingletonClass:
        raise NotImplementedError  # pragma: no cover


class PracticeBorgSingletonChild(PracticeBorgSingletonClass):
    def print_access(self) -> None:
        raise NotImplementedError  # pragma: no cover


class PracticeBorgSingletonResetChild(PracticeBorgSingletonClass):
    def print_access(self) -> None:
        raise NotImplementedError  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    print()
    normal = NormalClass()
    normal_child = NormalChild()
    normal_child2 = NormalChild()
    normal.set_access("Normalized")
    normal_child.set_access("Normalized Child")
    print("normal print():")
    normal.print_access()
    print("normal_child print():")
    normal_child.print_access()
    print("normal_child2 print():")
    normal_child2.print_access()
    print()

    singleton = SingletonClass()
    singleton_child = SingletonChild()
    singleton_child2 = SingletonChild()
    singleton.set_access("Singletoned")
    singleton_child.set_access("Singletoned Child")
    # singleton.print_access()
    # singleton_child.print_access()
    # singleton_child2.print_access()
    print()

    borg = BorgSingletonClass()
    borg_child = BorgSingletonChild()
    borg_child2 = BorgSingletonChild()
    borg.set_access("Borged")
    borg_child.set_access("Borged Child")
    # borg.print_access()
    borg_child.print_access()
    borg_child2.print_access()
