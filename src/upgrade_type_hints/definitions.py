# These are native types that can easily be replaced in-place
native_types: dict[str, str] = {
    'Dict': 'dict',
    'FrozenSet': 'frozenset',
    'List': 'list',
    'Set': 'set',
    'Tuple': 'tuple',
    'Type': 'type',
}

# These replacement require use to add an import,
# but are otherwise pretty straight forward
imported_types = {
    'Deque': {'from': 'collections', 'name': 'deque'},
    'DefaultDict': {'from': 'collections', 'name': 'defaultdict'},
    'AbstractSet': {'from': 'collections.abc', 'name': 'Set'},
    'ContextManager': {'from': 'contextlib', 'name': 'AbstractContextManager'},
    'AsyncContextManager': {'from': 'contextlib', 'name': 'AbstractAsyncContextManager'},
    're.Pattern': {'from': 're', 'name': 'Pattern'},
    're.Match': {'from': 're', 'name': 'Match'},
    'OrderedDict': {'from': 'collections', 'name': 'OrderedDict'},
    'Counter': {'from': 'collections', 'name': 'Counter'},
    'ChainMap': {'from': 'collections', 'name': 'ChainMap'},
    'Awaitable': {'from': 'collections.abc', 'name': 'Awaitable'},
    'Coroutine': {'from': 'collections.abc', 'name': 'Coroutine'},
    'AsyncIterable': {'from': 'collections.abc', 'name': 'AsyncIterable'},
    'AsyncIterator': {'from': 'collections.abc', 'name': 'AsyncIterator'},
    'AsyncGenerator': {'from': 'collections.abc', 'name': 'AsyncGenerator'},
    'Iterable': {'from': 'collections.abc', 'name': 'Iterable'},
    'Iterator': {'from': 'collections.abc', 'name': 'Iterator'},
    'Generator': {'from': 'collections.abc', 'name': 'Generator'},
    'Reversible': {'from': 'collections.abc', 'name': 'Reversible'},
    'Container': {'from': 'collections.abc', 'name': 'Container'},
    'Collection': {'from': 'collections.abc', 'name': 'Collection'},
    'Callable': {'from': 'collections.abc', 'name': 'Callable'},
    'MutableSet': {'from': 'collections.abc', 'name': 'MutableSet'},
    'Mapping': {'from': 'collections.abc', 'name': 'Mapping'},
    'MutableMapping': {'from': 'collections.abc', 'name': 'MutableMapping'},
    'Sequence': {'from': 'collections.abc', 'name': 'Sequence'},
    'MutableSequence': {'from': 'collections.abc', 'name': 'MutableSequence'},
    'ByteString': {'from': 'collections.abc', 'name': 'ByteString'},
    'MappingView': {'from': 'collections.abc', 'name': 'MappingView'},
    'KeysView': {'from': 'collections.abc', 'name': 'KeysView'},
    'ItemsView': {'from': 'collections.abc', 'name': 'ItemsView'},
    'ValuesView': {'from': 'collections.abc', 'name': 'ValuesView'},
    'Pattern': {'from': 're', 'name': 'Pattern'},
    'Match': {'from': 're', 'name': 'Match'},
}


def check_if_types_need_substitution(
    annotations: list[dict[str, str]], imports: list[dict]
) -> tuple[list, list]:
    """
    Checks whether the complete list of annotations contained in a file matches any of the pep-585-types
    we want to substitute.

    :return: We return a filtered list of dictionaries, where the dict has an
             extra attribute to indicate what it should be substituted with.
    """
    filtered_native_type_list = []
    filtered_import_list = []

    for item in annotations:
        stripped_annotation = item['annotation'].replace('typing.', '')
        if stripped_annotation in native_types:
            for _import in imports:
                if stripped_annotation in _import['names']:
                    item['new_annotation'] = native_types[stripped_annotation]
                    filtered_native_type_list.append(item)
                    break
        elif stripped_annotation in imported_types:
            for _import in imports:
                if stripped_annotation in _import['names']:
                    item['new_annotation'] = imported_types[stripped_annotation]['name']
                    item['import_from'] = imported_types[stripped_annotation]['from']
                    filtered_import_list.append(item)
                    break
    return filtered_native_type_list, filtered_import_list
