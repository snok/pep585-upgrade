import os

from tests import file_path

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

expectd = '''
from collections import ChainMap
from collections import OrderedDict
from collections.abc import Mapping
from collections import Counter
from collections import defaultdict
from collections.abc import Iterable
from collections import deque
import typing
from typing import (
)

x: int
x: float
x: bool
x: str
x: bytes
x: list
x: list
x: set
x: set
x: dict
x: dict
x: tuple
x: tuple
x: Iterable
x: Iterable
x: Mapping
x: Mapping
x: frozenset
x: frozenset
x: type
x: type
x: deque
x: deque
x: defaultdict
x: defaultdict
x: OrderedDict
x: OrderedDict
x: Counter
x: Counter
x: ChainMap
'''

result_path = file_path / 'result.py'
expected_path = file_path / 'expected.py'


def test_format_variables():
    with open(result_path, 'w+') as file:
        file.write(function_definition)

    with open(expected_path, 'w+') as file:
        file.write(expectd)

    # Execute the pre-commit hook as a CLI
    os.system(f'poetry run upgrade-type-hints-script {result_path}')

    # Load the changed file
    with open(result_path, 'rb') as f:
        # we need to sort the lines, since the imports get added randomly atm
        result = sorted(f.readlines())
    with open(expected_path, 'rb') as f:
        expected = sorted(f.readlines())

    result = [i for i in result if i.replace(b'\n', b'')]
    expected = [i for i in expected if i.replace(b'\n', b'')]

    for a, b in zip(result, expected):
        assert a == b

    os.remove(result_path)
    os.remove(expected_path)


def test_format_variables_with_futures():
    with open(result_path, 'w+') as file:
        file.write(function_definition)

    with open(expected_path, 'w+') as file:
        file.write(expectd)

    # Execute the pre-commit hook as a CLI
    os.system(f'poetry run upgrade-type-hints-script {result_path} --futures')

    # Load the changed file
    with open(result_path, 'rb') as f:
        # we need to sort the lines, since the imports get added randomly atm
        result = sorted(f.readlines())
    with open(expected_path, 'rb') as f:
        expected = sorted(f.readlines() + [b'from __future__ import annotations\n'])

    result = [i for i in result if i.replace(b'\n', b'')]
    expected = [i for i in expected if i.replace(b'\n', b'')]

    for a, b in zip(result, expected):
        assert a == b

    os.remove(result_path)
    os.remove(expected_path)
