class NormalClass(object):
    __class_var = None

    def __init__(self):
        self.__instance_var = None

    def set_access(self, value):
        self.__class_var = value
        self.__instance_var = value

    def get_class_access(self):
        return self.__class_var

    def get_instance_access(self):
        return self.__instance_var

    @staticmethod
    def print_access():
        print("Printed NormalClass")


class NormalChild(NormalClass):

    def print_access(self):
        print("Normal class_access = {}".format(self.get_class_access()))
        print("Normal instance_access = {}".format(self.get_instance_access()))


class SingletonClass(object):
    __class_var = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__instance_var = None

    def set_access(self, value):
        self.__class_var = value
        self.__instance_var = value

    def get_class_access(self):
        return self.__class_var

    def get_instance_access(self):
        return self.__instance_var

    # def print_access(self):
    #     print("Printed SingletonClass")


class SingletonChild(SingletonClass):

    def print_access(self):
        print("Singleton class_access = {}".format(self.get_class_access()))
        print("Singleton instance_access = {}".format(self.get_instance_access()))


class BorgSingletonClass(object):
    _shared_borg_state = {}
    __class_var = None

    def __new__(cls, *args, **kwargs):
        obj = super(BorgSingletonClass, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_borg_state
        return obj

    def __init__(self):
        self.__instance_var = None

    def set_access(self, value):
        self.__class_var = value
        self.__instance_var = value

    def get_class_access(self):
        return self.__class_var

    def get_instance_access(self):
        return self.__instance_var

    # def print_access(self):
    #     print("Printed BorgSingletonClass")


class BorgSingletonChild(BorgSingletonClass):

    def print_access(self):
        print("BorgSingleton class_access = {}".format(self.get_class_access()))
        print("BorgSingleton instance_access = {}".format(self.get_instance_access()))


class BorgSingletonResetChild(BorgSingletonClass):
    _shared_borg_state = {}

    def print_access(self):
        print("BorgSingleton class_access = {}".format(self.get_class_access()))
        print("BorgSingleton instance_access = {}".format(self.get_instance_access()))


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


class PracticeSingletonClass(object):

    def __new__(cls):
        raise NotImplementedError


class PracticeSingletonChild(PracticeSingletonClass):

    def print_access(self):
        raise NotImplementedError


class PracticeBorgSingletonClass(object):

    def __new__(cls, *args, **kwargs):
        raise NotImplementedError


class PracticeBorgSingletonChild(PracticeBorgSingletonClass):

    def print_access(self):
        raise NotImplementedError


class PracticeBorgSingletonResetChild(PracticeBorgSingletonClass):

    def print_access(self):
        raise NotImplementedError

