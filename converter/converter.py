from datetime import datetime
from time import sleep
from weakref import WeakKeyDictionary


class BitFieldBase:
    def __init__(self, **kwargs):
        self._validate_arg_names(kwargs)

        for field_name in type(self)._field_widths.keys():
            setattr(self, field_name, kwargs.get(field_name, 0))

    def _validate_arg_names(self, kwargs):
        mismatch_args = set(kwargs) - set(type(self)._field_widths)

        if len(mismatch_args) != 0:
            mismatched_args_txt = ", ".join(repr(arg_name) for arg_name in kwargs if arg_name in mismatch_args)

            raise TypeError(
                f'{type(self).__name__}.__init__() got unexpected'
                f' keyword argument{'' if len(mismatch_args) == 1 else 's'}: {mismatched_args_txt}'
            )

    def __int__(self):
        # TODO: repair adding sequence of types
        accumulator = 0
        shift = 0

        for name, width in type(self)._field_widths.items():
            value = getattr(self, name)
            accumulator |= value << shift
            shift += width
        return accumulator

    def to_bytes(self):
        v = int(self)
        num_bytes = (sum(type(self)._field_widths.values()) + 7) // 8
        return v.to_bytes(
            length=num_bytes,
            byteorder='little',
            signed=False,
        )


class BitFieldDescriptor:
    def __init__(self, name, width):
        self._instance_data = WeakKeyDictionary()
        self._name = name
        self._width = width

    def __get__(self, instance, owner):
        return self._instance_data[instance]

    def __set__(self, instance, value):
        min_value = 0
        max_value = 2 ** self._width - 1
        if not (min_value <= value <= max_value):
            raise ValueError(
                f"{type(instance).__name__} field {self._name!r} "
                f"got value {value!r} which is out of "
                f"range {min_value}-{max_value} for a {self._width} bit field"
            )
        self._instance_data[instance] = value


class BitFieldMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        try:
            namespace["_field_widths"] = namespace["__annotations__"]
        except KeyError as e:
            raise TypeError(f'{name} with metaclass "{mcs.__name__}" has no fields.') from e

        for field_name, width in namespace['_field_widths'].items():
            if field_name.startswith('_'):
                raise TypeError(
                    f"{name} field {field_name!r} begins with an underscore"
                )

            if not isinstance(width, int):
                raise TypeError(
                    f"{name} field {field_name!r} has annotation {width!r} that is not an integer"
                )

            if width < 1:
                raise TypeError(
                    f"{name} field {field_name!r} has non-positive field width {width!r}"
                )

        for field_name, width in namespace["_field_widths"].items():
            namespace[field_name] = BitFieldDescriptor(field_name, width)

        bases = (BitFieldBase,) + bases
        return super().__new__(mcs, name, bases, namespace)



class DS3231Registers(metaclass=BitFieldMeta):
    seconds_1: 4
    seconds_10: 3
    seconds_pad: 1

    minutes_1: 4
    minutes_10: 3
    minutes_pad: 1

    hour_1: 4
    hour_10: 2
    hour_12_24: 1
    hour_pad: 1

    day_1: 3
    day_pad: 5

    date_1: 4
    date_10: 2
    date_pad: 2

    month_1: 4
    month_10: 1
    month_pad: 2
    century: 1

    year_1: 4
    year_10: 4



def ds3231_registers(d):

    registers = DS3231Registers(
            seconds_1 = d.second % 10,
            seconds_10 = d.second // 10,
            minutes_1 = d.minute % 10,
            minutes_10 = d.minute // 10,
            hour_1 = d.hour % 10,
            hour_10 = d.hour // 10,
            hour_12_24 = 0,
            day_1 = d.isoweekday(),
            date_1 = d.day % 10,
            date_10 = d.day // 10,
            month_1 = d.month % 10,
            month_10 = d.month // 10,
            century = 0,
            year_1 = d.year % 10,
            year_10 = d.year // 10 % 10
        )

    return registers.to_bytes()


if __name__ == '__main__':
    for d in iter(datetime.now, None):
        registers = ds3231_registers(d)
        print(" ".join(f"{register:08b}" for register in registers))
        sleep(1.0)