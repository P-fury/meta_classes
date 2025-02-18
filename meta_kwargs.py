class EntriesMeta(type):

    def __new__(mcs, name, bases, namespace, **kwargs):
        num_entries = kwargs["num_entries"]

        namespace.update(
            {chr(i): i for i in range(ord('a'), ord('a')+num_entries)}
        )

        return super().__new__(mcs, name, bases, namespace)



class AZ(metaclass=EntriesMeta, num_entries=26):
    pass


print(dir(AZ))
print(AZ.num_entries)