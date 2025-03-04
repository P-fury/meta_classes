import re

import pytest

from converter.converter import BitFieldMeta

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


def test_assigning_to_field_sets_values():
    class DateBitField(metaclass=BitFieldMeta):
        day: 5

    d = DateBitField()
    d.day = 26
    assert d.day == 26


def test_assigning_out_of_upper_range_value_to_field_raises_type_error():
    class DateBitField(metaclass=BitFieldMeta):
        day: 5

    d = DateBitField()

    with pytest.raises(ValueError, match=re.escape("DateBitField field 'day' got value 32 which is out"
                                                   " of range 0-31 for a 5 bit field")):
        d.day = 32


# TODO: validate field values are integers
# TODO: named constructor to construct from in or bytes objects
# TODO: support a metaclass keyword argument revers=True to reverse field order
# TODO: provide endianness control when converting bitfields to integers
# TODO: prevent field deletion by overriding __delete__ on the descriptor
class DateBitField(metaclass=BitFieldMeta):
    day: 5