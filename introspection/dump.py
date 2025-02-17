import inspect
from itertools import chain


def dump(obj):
    print("Type")
    print("====")
    print(type(obj))
    print()

    print("Documentation")
    print("=============")
    print(inspect.getdoc(obj))
    print()

    all_attr_names = set(dir(obj))

    method_names: set = set(
        filter(lambda attr_name: callable(getattr(obj, attr_name)), all_attr_names)
    )

    assert method_names <= all_attr_names
    attr_names = all_attr_names - method_names

    print("Attributes")
    print("=============")
    attr_names_and_values = [(name, getattr(obj, name)) for name in attr_names]
    print_table(attr_names_and_values, "Name", "Value")
    print()


def print_table(rows_of_columns, *headers):

    num_columns = len(rows_of_columns[0])
    num_headers = len(headers)

    if num_headers != num_columns:
        raise ValueError(f"Expected {num_columns} header arguments, got {num_headers} instead.")

    rows_of_columns_with_header = chain([headers], rows_of_columns)
    columns_of_rows = list(zip(*rows_of_columns_with_header))
    columns_widths = [max(map(lambda x: len(str(x)), column)) for column in columns_of_rows]
    column_specs = list(('{{:{w}}}'.format(w=width) for width in columns_widths))
    format_spec = ' '.join(column_specs)
    print(format_spec.format(*headers))
    rules = ('-' * width for width in columns_widths)
    print(format_spec.format(*rules))
    for row in rows_of_columns:
        print(format_spec.format(*row))


if __name__ == '__main__':
    dump(4)