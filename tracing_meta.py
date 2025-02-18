class TracingMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        print("TracingMeta.__prepare__")
        print(f"{mcs = }")
        print(f"{name = }")
        print(f"{bases = }")
        print(f"{kwargs = }")
        namespace = super().__prepare__(name, bases)
        print(f"{namespace = }")
        print()
        return namespace

    def __new__(mcs, name, bases, namespace, **kwargs):
        print("TracingMeta.__new__")
        print(f"{mcs = }")
        print(f"{name = }")
        print(f"{bases = }")
        print(f"{namespace = }")
        print(f"{kwargs = }")
        cls = super().__new__(mcs, name, bases, namespace)
        print(f"{cls = }")
        print()
        return cls

    def __init__(cls, name, bases, namespace, **kwargs):
        print("TracingMeta.__init__")
        print(f"{cls = }")
        print(f"{name = }")
        print(f"{bases = }")
        print(f"{namespace = }")
        print(f"{kwargs = }")
        super().__init__(name, bases, namespace)

        print()

    def metamethod(cls):
        print("TracingMeta.metamethod")
        print(f"{cls=}")


class TracingSpecialMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        print("TracingSpecialMeta.__new__")
        print(f"{mcs = }")
        print(f"{name = }")
        print(f"{bases = }")
        print(f"{namespace = }")
        print(f"{kwargs = }")
        cls = super().__new__(mcs, name, bases, namespace)
        print(f"{cls = }")
        print()
        return cls


class TracingPro(TracingMeta, TracingSpecialMeta):
    pass


class Widget(object, metaclass=TracingMeta, magic=42):
    the_answer = 42

    def action(self, message):
        print(message)


class SpecialWidget(Widget, metaclass=TracingPro):
    pass


Widget.metamethod()
SpecialWidget.metamethod()

w = Widget()
# w.metamethod()
# w.action('42')
