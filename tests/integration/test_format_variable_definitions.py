import os

from tests import file_path

example_file = file_path / 'example_files/expected_variable_definitions.py'
project_dir = file_path.parent

function_definition = '''
import typing
from typing import ChainMap, Counter
from typing import (
    DefaultDict,
    Deque,
    Dict,
    FrozenSet,
    Iterable,
    List,
    Mapping,
    OrderedDict,
    Set,
    Tuple,
    Type,
)

x: int
x: float
x: bool
x: str
x: bytes
x: List
x: typing.List
x: Set
x: typing.Set
x: Dict
x: typing.Dict
x: Tuple
x: typing.Tuple
x: Iterable
x: typing.Iterable
x: Mapping
x: typing.Mapping
x: FrozenSet
x: typing.FrozenSet
x: Type
x: typing.Type
x: Deque
x: typing.Deque
x: DefaultDict
x: typing.DefaultDict
x: OrderedDict
x: typing.OrderedDict
x: Counter
x: typing.Counter
x: ChainMap
'''


def test_format_variables():
    path = file_path / 'temp/test_format_variables.py'
    with open(path, 'w+') as file:
        file.write(function_definition)

    # Execute the pre-commit hook as a CLI
    os.system(f'poetry run upgrade-type-hints-script {path}')

    # Load the changed file
    with open(path, 'rb') as f:
        # we need to sort the lines, since the imports get added randomly atm
        result = sorted(f.readlines())
    with open(example_file, 'rb') as f:
        expected = sorted(f.readlines())

    result = [i for i in result if i.replace(b'\n', b'')]
    expected = [i for i in expected if i.replace(b'\n', b'')]

    for a, b in zip(result, expected):
        assert a == b

    os.remove(path)


def test_format_variables_with_futures():
    path = file_path / 'temp/test_format_variables.py'
    with open(path, 'w+') as file:
        file.write(function_definition)

    # Execute the pre-commit hook as a CLI
    os.system(f'poetry run upgrade-type-hints-script {path} --futures=true')

    # Load the changed file
    with open(path, 'rb') as f:
        # we need to sort the lines, since the imports get added randomly atm
        result = sorted(f.readlines())
    with open(example_file, 'rb') as f:
        expected = sorted(f.readlines() + [b'from __future__ import annotations\n'])

    result = [i for i in result if i.replace(b'\n', b'')]
    expected = [i for i in expected if i.replace(b'\n', b'')]

    for a, b in zip(result, expected):
        assert a == b

    os.remove(path)
