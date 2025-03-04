from weakref import WeakKeyDictionary

class BitFieldDescriptor(property):
    def __init__(self, *args, **kwargs):
        self._instance_data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        print('getter')
        return self._instance_data[instance]

    def __set__(self, instance, value):
        print('setter')
        self._instance_data[instance] = value


class Magic:
    def __init__(self):
        self.value_1 = 42
        self.value_2 = 2137

    @BitFieldDescriptor
    def value_1(self):
        return self._value_1

    @value_1.setter
    def value_1(self, value):
        self._value_1 = value

m = Magic()