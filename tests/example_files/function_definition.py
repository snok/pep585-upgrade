import re
import typing
from collections import ChainMap, Counter, OrderedDict, deque
from collections.abc import (
    AsyncGenerator,
    AsyncIterator,
    Callable,
    Collection,
    Container,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    Mapping,
    MutableMapping,
    MutableSet,
    Reversible,
    Sequence,
    Set,
    ValuesView,
)
from contextlib import AbstractAsyncContextManager
from re import Match, Pattern
from typing import Union


def very_complex_function(
    a: typing.Tuple[list[dict[set[frozenset[type, deque]]]]],
    b: typing.DefaultDict[OrderedDict[Counter, ChainMap]],
    c: typing.Awaitable,
    d: typing.Coroutine,
    e: typing.AsyncIterable[AsyncIterator[AsyncGenerator[Iterable, Iterator]]],
    f: typing.Generator[Reversible],
    g: typing.Union[Callable, Set],
    h: typing.Union[MutableSet[Mapping, MutableMapping], Sequence],
    i: typing.MutableSequence[Container[Collection]],
    j: typing.ByteString,
    k: typing.MappingView[KeysView[ItemsView[ValuesView]]],
    l: typing.ContextManager,
    m: typing.Optional[AbstractAsyncContextManager],
) -> Union[Pattern, Match]:
    return re.compile(f'{a},{b},{c},{d},{e},{f},{g},{h},{i},{j},{k},{l},{m}')
