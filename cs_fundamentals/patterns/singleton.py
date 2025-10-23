from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, ClassVar, Self


class NormalClass:
    __class_var: ClassVar[str | None] = None

    def __init__(self) -> None:
        self.__instance_var: str | None = None

    def set_access(self, value: str) -> None:
        self.__class_var = value
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


class SingletonClass:
    __class_var: ClassVar[str | None] = None

    def __new__(cls: Self) -> Self:
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.__instance_var: str | None = None

    def set_access(self, value: str) -> None:
        self.__class_var = value
        self.__instance_var = value

    def get_class_access(self) -> str | None:
        return self.__class_var

    def get_instance_access(self) -> str | None:
        return self.__instance_var

    # def print_access(self) -> None:
    #     print("Printed SingletonClass")


class SingletonChild(SingletonClass):
    def print_access(self) -> None:
        print(f"Singleton class_access = {self.get_class_access()}")
        print(f"Singleton instance_access = {self.get_instance_access()}")


class BorgSingletonClass:
    _shared_borg_state: dict[str, Any] = {}
    __class_var: ClassVar[str | None] = None

    def __new__(cls: type[Self], *args: Any, **kwargs: Any) -> Self:
        obj = super().__new__(cls)
        obj.__dict__ = cls._shared_borg_state
        return obj

    def __init__(self) -> None:
        self.__instance_var: str | None = None

    def set_access(self, value: str) -> None:
        self.__class_var = value
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
    _shared_borg_state: dict[str, Any] = {}

    def print_access(self) -> None:
        print(f"BorgSingleton class_access = {self.get_class_access()}")
        print(f"BorgSingleton instance_access = {self.get_instance_access()}")


class PracticeSingletonClass:
    def __new__(cls: type[Self]) -> Self:
        raise NotImplementedError


class PracticeSingletonChild(PracticeSingletonClass):
    def print_access(self) -> None:
        raise NotImplementedError


class PracticeBorgSingletonClass:
    def __new__(cls: type[Self], *args: Any, **kwargs: Any) -> Self:
        raise NotImplementedError


class PracticeBorgSingletonChild(PracticeBorgSingletonClass):
    def print_access(self) -> None:
        raise NotImplementedError


class PracticeBorgSingletonResetChild(PracticeBorgSingletonClass):
    def print_access(self) -> None:
        raise NotImplementedError


if __name__ == "__main__":
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
