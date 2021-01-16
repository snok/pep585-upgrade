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
    g: typing.Union[Callable, Set],
    h: typing.Union[MutableSet[Mapping, MutableMapping], Sequence],
    i: MutableSequence[Container[Collection]],
    j: ByteString,
    k: MappingView[KeysView[ItemsView[ValuesView]]],
    l: AbstractContextManager,
    m: typing.Optional[AbstractAsyncContextManager],
) -> Union[Pattern, Match]:
    return re.compile(f'{a},{b},{c},{d},{e},{f},{g},{h},{i},{j},{k},{l},{m}')
