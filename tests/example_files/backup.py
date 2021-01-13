import re
import typing
from typing import (
    AbstractSet,
    AsyncContextManager,
    AsyncGenerator,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    ByteString,
    Callable,
    ChainMap,
    Collection,
    Container,
    ContextManager,
    Coroutine,
    Counter,
    DefaultDict,
    Deque,
    Dict,
    FrozenSet,
    Generator,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    List,
    Mapping,
    MappingView,
    Match,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Optional,
    OrderedDict,
    Pattern,
    Reversible,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
    ValuesView,
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


def very_complex_function(
    a: Tuple[List[Dict[Set[FrozenSet[Type, Deque]]]]],
    b: DefaultDict[OrderedDict[Counter, ChainMap]],
    c: Awaitable,
    d: Coroutine,
    e: AsyncIterable[AsyncIterator[AsyncGenerator[Iterable, Iterator]]],
    f: Generator[Reversible],
    g: Union[Callable, AbstractSet],
    h: Union[MutableSet[Mapping, MutableMapping], Sequence],
    i: MutableSequence[Container[Collection]],
    j: ByteString,
    k: MappingView[KeysView[ItemsView[ValuesView]]],
    l: ContextManager,
    m: Optional[AsyncContextManager],
) -> Union[Pattern, Match]:
    return re.compile(f'{a},{b},{c},{d},{e},{f},{g},{h},{i},{j},{k},{l},{m}')
