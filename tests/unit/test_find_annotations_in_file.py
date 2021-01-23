from src.upgrade_type_hints.checker import find_annotations_and_imports_in_file

from .. import file_path


def test_find_type_annotations_in_file():
    annotations, _, _ = find_annotations_and_imports_in_file(
        file_path / 'example_files/function_definition_template.py'
    )
    just_annotations = [i['annotation'] for i in annotations]
    assert just_annotations.count('typing.Tuple') == 1
    assert just_annotations.count('List') == 1
    assert just_annotations.count('Dict') == 1
    assert just_annotations.count('Set') == 1
    assert just_annotations.count('FrozenSet') == 1
    assert just_annotations.count('Type') == 1
    assert just_annotations.count('Deque') == 1
    assert just_annotations.count('typing.DefaultDict') == 1
    assert just_annotations.count('OrderedDict') == 1
    assert just_annotations.count('Counter') == 1
    assert just_annotations.count('ChainMap') == 1
    assert just_annotations.count('typing.Awaitable') == 1
    assert just_annotations.count('typing.Coroutine') == 1
    assert just_annotations.count('typing.AsyncIterable') == 1
    assert just_annotations.count('AsyncIterator') == 1
    assert just_annotations.count('AsyncGenerator') == 1
    assert just_annotations.count('Iterable') == 1
    assert just_annotations.count('typing.Generator') == 1
    assert just_annotations.count('Reversible') == 1
    assert just_annotations.count('typing.Union') == 2
    assert just_annotations.count('Union') == 1
    assert just_annotations.count('Callable') == 1
    assert just_annotations.count('AbstractSet') == 1
    assert just_annotations.count('MutableSet') == 1
    assert just_annotations.count('Mapping') == 1
    assert just_annotations.count('MutableMapping') == 1
    assert just_annotations.count('Sequence') == 1
    assert just_annotations.count('typing.MutableSequence') == 1
    assert just_annotations.count('Container') == 1
    assert just_annotations.count('Collection') == 1
    assert just_annotations.count('typing.ByteString') == 1
    assert just_annotations.count('typing.MappingView') == 1
    assert just_annotations.count('KeysView') == 1
    assert just_annotations.count('ItemsView') == 1
    assert just_annotations.count('ValuesView') == 1
    assert just_annotations.count('typing.ContextManager') == 1
    assert just_annotations.count('typing.Optional') == 1
    assert just_annotations.count('AsyncContextManager') == 1
    assert just_annotations.count('Pattern') == 1
    assert just_annotations.count('Match') == 1
