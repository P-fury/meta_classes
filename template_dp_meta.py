class PhasedMeta(type):
    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls, *args, **kwargs)
        obj._pre_init(*args, **kwargs)
        obj.__init__(*args, **kwargs)
        obj._post_init(*args, **kwargs)
        return obj

class PhasedInit(metaclass=PhasedMeta):

    def _pre_init(self):
        print('pre init...')

    def __init__(self):
        print('do init...')

    def _post_init(self):
        print('post init...')


class SubPhasedInit(PhasedInit):
    def __init__(self):
        super().__init__()
        print('do sub init...')


s = SubPhasedInit()

# print(s)
