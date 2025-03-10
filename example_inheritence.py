class MetaA(type):
    pass


class MetaB(type):
    pass

class MetaC(MetaA, MetaB):
    pass

class A(metaclass=MetaA):
    pass


class B(metaclass=MetaB):
    pass


class C(A, B, metaclass=MetaC):
    pass


class D(A):
    pass

print(type(C))
print(type(D))
