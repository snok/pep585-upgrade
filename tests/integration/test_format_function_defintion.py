import os

from tests import file_path

function_definition = '''
import re
import typing
from typing import (
    AbstractSet,
    AsyncContextManager,
    AsyncGenerator,
    AsyncIterator,
    Callable,
    ChainMap,
    Collection,
    Container,
    Counter,
    Deque,
    Dict,
    FrozenSet,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    List,
    Mapping,
    Match,
    MutableMapping,
    MutableSet,
    OrderedDict,
    Pattern,
    Reversible,
    Sequence,
    Set,
    Type,
    Union,
    ValuesView,
)


def very_complex_function(
    a: typing.Tuple[List[Dict[Set[FrozenSet[Type, Deque]]]]],
    b: typing.DefaultDict[OrderedDict[Counter, ChainMap]],
    c: typing.Awaitable,
    d: typing.Coroutine,
    e: typing.AsyncIterable[AsyncIterator[AsyncGenerator[Iterable, Iterator]]],
    f: typing.Generator[Reversible],
    g: typing.Union[Callable, AbstractSet],
    h: typing.Union[MutableSet[Mapping, MutableMapping], Sequence],
    i: typing.MutableSequence[Container[Collection]],
    j: typing.ByteString,
    k: typing.MappingView[KeysView[ItemsView[ValuesView]]],
    l: typing.ContextManager,
    m: typing.Optional[AsyncContextManager],
) -> Union[Pattern, Match]:
    return re.compile(f'{a},{b},{c},{d},{e},{f},{g},{h},{i},{j},{k},{l},{m}')
'''

expectd = '''
from collections.abc import MutableSet
from collections.abc import MutableMapping
from collections.abc import Sequence
from collections import OrderedDict
from collections.abc import MappingView
from collections.abc import Coroutine
from collections.abc import Iterator
from collections.abc import Iterable
from contextlib import AbstractContextManager
from contextlib import AbstractAsyncContextManager
from collections.abc import AsyncGenerator
from re import Pattern
from collections.abc import ValuesView
from collections.abc import ItemsView
from collections.abc import Mapping
from collections.abc import Collection
from collections import ChainMap
from re import Match
from collections.abc import Callable
from collections.abc import ByteString
from collections import deque
from collections.abc import KeysView
from collections.abc import Reversible
from collections.abc import AsyncIterable
from collections.abc import MutableSequence
from collections.abc import Set
from collections.abc import Awaitable
from collections import defaultdict
from collections import Counter
from collections.abc import Container
from collections.abc import Generator
from collections.abc import AsyncIterator

import re
import typing
from typing import (
    Union,
)


def very_complex_function(
    a: tuple[list[dict[set[frozenset[type, deque]]]]],
    b: defaultdict[OrderedDict[Counter, ChainMap]],
    c: Awaitable,
    d: Coroutine,
    e: AsyncIterable[AsyncIterator[AsyncGenerator[Iterable, Iterator]]],
    f: Generator[Reversible],
    g: typing.Union[Callable, Set],
    h: typing.Union[MutableSet[Mapping, MutableMapping], Sequence],
    i: MutableSequence[Container[Collection]],
    j: ByteString,
    k: MappingView[KeysView[ItemsView[ValuesView]]],
    l: AbstractContextManager,
    m: typing.Optional[AbstractAsyncContextManager],
) -> Union[Pattern, Match]:
    return re.compile(f'{a},{b},{c},{d},{e},{f},{g},{h},{i},{j},{k},{l},{m}')
'''

result_path = file_path / 'result.py'
expected_path = file_path / 'expected.py'


def test_format_function_definition():
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


def test_format_function_definition_with_futures():
    with open(result_path, 'w+') as file:
        file.write(function_definition)
    with open(expected_path, 'w+') as file:
        file.write(expectd)

    # Execute the pre-commit hook as a CLI
    os.system(f'poetry run upgrade-type-hints-script {result_path} --futures=true')

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
