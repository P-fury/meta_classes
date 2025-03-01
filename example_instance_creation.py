class MetaKwargs(type):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        d = super().__prepare__(mcs, name, bases)
        print(kwargs)

        return d

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args)

    @classmethod
    def __init__(cls, *args, **kwargs):
        super().__init__(cls, *args, **kwargs)


class Yolo(metaclass=MetaKwargs, secret_pass='TestPass123!'):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


x = Yolo()
