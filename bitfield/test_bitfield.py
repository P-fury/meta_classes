import re

import pytest


class BitFieldBase:
    def __init__(self, **kwargs):
        self._validate_arg_names(kwargs)
        self._validate_arg_values(kwargs)

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

    def _validate_arg_values(self, kwargs):
        for keyword, value in kwargs.items():
            width = type(self)._field_widths[keyword]
            min_value = 0
            max_value = 2 ** width - 1
            if not (min_value <= value <= max_value):
                raise ValueError(
                    f"{type(self).__name__} field {keyword!r} "
                    f"got value {value!r} which is out of "
                    f"range {min_value}-{max_value} for a {width} bit field"
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

        bases = (BitFieldBase,) + bases
        return super().__new__(mcs, name, bases, namespace)


def test_define_bitfield():
    class DateBitField(metaclass=BitFieldMeta):
        day: 5


def test_instantiate_default_bitfield():
    class DateBitField(metaclass=BitFieldMeta):
        day: 5

    _ = DateBitField(day=23)


def test_bitfield_without_fields_raises_type_error():
    with pytest.raises(TypeError, match=f'EmptyBitField with metaclass "BitFieldMeta" has no fields.'):
        class EmptyBitField(metaclass=BitFieldMeta):
            pass


def test_mismatched_constructor_argument_names_raises_type_error():
    class DateBitField(metaclass=BitFieldMeta):
        day: 5
        month: 4
        year: 14

    with pytest.raises(TypeError,
                       match=re.escape(f"DateBitField.__init__() got unexpected keyword arguments: 'mnth', 'yr'")):
        DateBitField(day=5, mnth=4, yr=1994)


def test_non_integer_annotation_value_raises_type_error():
    with pytest.raises(TypeError,
                       match=re.escape("DateBitField field 'day' has annotation 'Wednesday' that is not an integer")):
        class DateBitField(metaclass=BitFieldMeta):
            day: "Wednesday"


def test_negative_field_width_raises_type_error():
    with pytest.raises(TypeError,
                       match=re.escape("DateBitField field 'day' has non-positive field width -1")):
        class DateBitField(metaclass=BitFieldMeta):
            day: -1


def test_field_name_with_leading_undersocre_raises_type_error():
    with pytest.raises(TypeError,
                       match=re.escape("DateBitField field '_day' begins with an underscore")):
        class DateBitField(metaclass=BitFieldMeta):
            _day: 5


def test_initialization_out_of_upper_field_range_raises_value_error():
    class DateBitField(metaclass=BitFieldMeta):
        day: 5

    with pytest.raises(ValueError, match=re.escape("DateBitField field 'day' got value 32 which is out"
                                                   " of range 0-31 for a 5 bit field")):
        DateBitField(day=32)


def test_fields_are_default_initialized_to_zero():
    class DateBitField(metaclass=BitFieldMeta):
        day: 5

    d = DateBitField()
    assert d.day == 0


def test_initialized_field_values_can_be_retrieved():
    class DateBitField(metaclass=BitFieldMeta):
        day: 5
        month: 4
        year: 14

    d = DateBitField(month=5, year=14)
    assert d.day == 0 and d.month == 5 and d.year == 14


def test_conversion_to_integer():
    class DateBitField(metaclass=BitFieldMeta):
        day: 5
        month: 4
        year: 14

    d = DateBitField(day=25, month=3, year=2010)
    i = int(d)

    assert i == 0b00011111011010_0011_11001
    # year_month_day


def test_conversion_to_bytes():
    class DateBitField(metaclass=BitFieldMeta):
        day: 5
        month: 4
        year: 14

    d = DateBitField(day=25, month=3, year=2010)
    b = d.to_bytes()

    assert b == (0b00011111011010_0011_11001).to_bytes(3, 'little', signed=False)
    # year_month_day
