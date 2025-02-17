class Widget(object, metaclass=type):
    pass


w = Widget()

name = "Widget2"
metaclass = type
bases = ()
kwargs = {}

namespace = metaclass.__prepare__(name, bases, **kwargs)
Widget2 = metaclass.__new__(metaclass, name, bases, namespace, **kwargs)
metaclass.__init__(Widget2, name, bases, namespace, **kwargs)

w2 = Widget2
# print(w2)