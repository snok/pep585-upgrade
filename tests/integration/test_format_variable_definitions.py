from tests.integration import int_test

variables_definition = '''
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
import typing
from collections import ChainMap, Counter, OrderedDict, defaultdict, deque
from collections.abc import Iterable, Mapping

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


def test_format_variables():
    int_test(variables_definition, expectd)
    int_test(variables_definition, expectd, futures=True)
