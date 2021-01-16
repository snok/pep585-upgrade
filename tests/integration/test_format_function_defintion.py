import os

from tests import file_path

example_file = file_path / 'example_files/expected_function_definition.py'
project_dir = file_path.parent

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


def test_format_function_definition():
    path = file_path / 'temp/test_format_function.py'
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

    for i in result:
        print(i)
    print('--')
    for i in expected:
        print(i)

    for a, b in zip(result, expected):
        assert a == b
