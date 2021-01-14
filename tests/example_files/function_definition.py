from collections.abc import Callable
from collections.abc import Sequence
from re import Match
from collections.abc import ValuesView
from collections.abc import Awaitable
from collections import Counter
from collections.abc import MutableMapping
from collections.abc import ByteString
from collections.abc import AsyncIterator
from collections.abc import Generator
from collections.abc import AsyncIterable
from collections.abc import AsyncGenerator
from collections.abc import Iterator
from collections.abc import Mapping
from collections.abc import Collection
from re import Pattern
from collections.abc import MutableSet
from collections.abc import MappingView
from collections import ChainMap
from collections.abc import Coroutine
from collections.abc import KeysView
from collections import OrderedDict
from collections.abc import ItemsView
from collections.abc import Reversible
from collections.abc import Iterable
from collections.abc import Container
from collections.abc import MutableSequence
import re
import typing
from collections import ChainMap, Counter, OrderedDict, defaultdict, deque
from collections.abc import (
    AsyncGenerator,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    ByteString,
    Callable,
    Collection,
    Container,
    Coroutine,
    Generator,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    Mapping,
    MappingView,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Reversible,
    Sequence,
    Set,
    ValuesView,
)
from contextlib import AbstractAsyncContextManager, AbstractContextManager
from re import Match, Pattern
from typing import Union


def very_complex_function(
    a: tuple[list[dict[set[frozenset[type, deque]]]]],
    b: defaultdict[OrderedDict[Counter, ChainMap]],
    c: Awaitable,
    d: Coroutine,
    e: AsyncIterable[AsyncIterator[AsyncGenerator[Iterable, Iterator]]],
    f: Generator[Reversible],
    g: typing.Union[Callable, set],
    h: typing.Union[MutableSet[Mapping, MutableMapping], Sequence],
    i: MutableSequence[Container[Collection]],
    j: ByteString,
    k: MappingView[KeysView[ItemsView[ValuesView]]],
    l: AbstractContextManager,
    m: typing.Optional[AbstractAsyncContextManager],
) -> Union[Pattern, Match]:
    return re.compile(f'{a},{b},{c},{d},{e},{f},{g},{h},{i},{j},{k},{l},{m}')
