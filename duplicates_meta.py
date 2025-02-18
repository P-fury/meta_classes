class OneShotNamespace(dict):
    def __init__(self,name, existing=None):
        super().__init__()
        self._name = name
        if existing is not None:
            for k, v in existing.items():
                self[k] = v

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(
                f"Cannot reassign attribute: {key!r} "
                f"of class: {self._name!r}"
            )
        super().__setitem__(key, value)

class ProhibitDuplicatesMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        return OneShotNamespace(name)

osd = OneShotNamespace({"a":1, "b":2, "c":3, "d":4})
# osd["a"] = 5
print(osd)



class Dodgy(metaclass=ProhibitDuplicatesMeta):
    def method(self):
        return "first definition"

    def method(self):
        return "second definition"
