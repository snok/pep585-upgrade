from __future__ import annotations

import argparse
import re
from typing import Optional, Sequence

native_types: dict[str, str] = {
    # Types that do not require additional imports
    # and can easily be added using simple replacement
    'Dict': 'dict',
    'FrozenSet': 'frozenset',
    'List': 'list',
    'Set': 'set',
    'Tuple': 'tuple',
    'Type': 'type',
}

imported_types: dict[str, dict[str, str]] = {
    # Types that require an import at the top level of a file
    'Deque': {'from': 'collections', 'name': 'deque'},
    'DefaultDict': {'from': 'collections', 'name': 'defaultdict'},
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
    'AbstractSet': {'from': 'collections.abc', 'name': 'Set'},
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
    'ContextManager': {'from': 'contextlib', 'name': 'AbstractContextManager'},
    'AsyncContextManager': {'from': 'contextlib',
                            'name': 'AbstractAsyncContextManager'},
    're.Pattern': {'from': 're', 'name': 'Pattern'},
    'Pattern': {'from': 're', 'name': 'Pattern'},
    're.Match': {'from': 're', 'name': 'Match'},
    'Match': {'from': 're', 'name': 'Match'},
}


def pattern_generator(types: dict[str, any]) -> re.Pattern:
    """
    A generalised regex pattern will help us quickly flag lines which should be handled.

    :param types: dictionary containing the old type names
    :return: a regex pattern to detect when old types are present in a file line
    """
    # \s? is optional whitespace
    # : or -> is expected before type annotation

    # The full pattern for the native types looks like this
    # \s?(:|->)\s?(Dict|typing.Dict|FrozenSet|typing.FrozenSet|List|typing.List|Set|typing.Set|Tuple|typing.Tuple)
    # We're looking for patterns like ` : typing.Dict`, `->dict`, etc.

    pattern = ''
    for type_name in types:
        if pattern:
            pattern += r'|{type_name}|typing.{type_name}'.format(
                type_name=type_name)
        else:
            pattern += r'{type_name}|typing.{type_name}'.format(
                type_name=type_name)
    combined_pattern = fr'(\[|->\s?|:\s?|,\s?)({pattern})\['
    return re.compile(bytes(combined_pattern, encoding='utf-8'))


native_type_pattern = pattern_generator(native_types)
imported_type_pattern = pattern_generator(imported_types)

def clean(s: bytes) -> bytes:
    regex = re.compile(b'[^a-zA-Z]')
    return regex.sub(b'', s)

def process_line(line: bytes) -> tuple[bytes, set[tuple[bytes, bytes]], bool]:
    """
    Finds replacement candidates.

    :return: List of matches, where each match is represented by a set
            containing:
        - A set containing the starting and ending index of the candidate
        - The old name
        - The name of the new type it should be replaced with
        - The import that has to be made at the top level
    """
    upgraded = False
    imports = set()
    for m in re.finditer(native_type_pattern, line):
        match = line[m.start(0): m.end(0)].replace(b'typing.', b'')
        old_type = clean(match)
        new_type = native_types[old_type.decode()].encode('utf-8')
        new_val = match.replace(old_type, new_type)
        line = line[: m.start(0)] + new_val + line[m.end(0):]
        upgraded = True
    for m in re.finditer(imported_type_pattern, line):
        match = line[m.start(0): m.end(0)].replace(b'typing.', b'')
        old_type = clean(match)
        new_obj = imported_types[old_type.decode()]
        new_type = new_obj['name'].encode('utf-8')
        new_val = match.replace(old_type, new_type)
        line = line[: m.start(0)] + new_val + line[m.end(0):]
        upgraded = True
        imports.add((new_obj['from'].encode('utf-8'), new_type))

    return line, imports, upgraded


def fix_file(filename: str, futures: bool) -> bool:
    """
    Iterates through a files lines and upgrades type
    annotations when upgrade candidates are found.
    """
    any_file_upgraded = False

    with open(filename, mode='rb+') as file:
        # Read the file
        content = file.readlines()

        # Define initial values for imports we need to add at the end
        unique_imports: set[tuple[bytes, bytes]] = set()

        file_upgraded = False
        for line_no, line in enumerate(content):

            # Fetch upgrade candidates for individual lines
            line, imports, upgraded = process_line(line)

            if upgraded:
                any_file_upgraded = True
                file_upgraded = True
                content[line_no] = line
                if imports:
                    unique_imports.update(imports)

        if file_upgraded:
            # Only need to print once per file, so move this out
            print(f'Upgrading types in {filename}')

        concat_imports = list(
            {b'from ' + _from + b' import ' + _name + b'\n' for (_from, _name)
             in unique_imports}
        )
        if futures:
            concat_imports = [
                                 b'from __future__ import annotations\n\n'] + concat_imports
    with open(filename, 'wb') as file:
        file.writelines(concat_imports + content)

    return any_file_upgraded


def str_to_bool(v):
    # Stolen from https://stackoverflow.com/questions/
    # 15008758/parsing-boolean-values-with-argparse
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to run')
    parser.add_argument(
        'futures',
        type=str_to_bool,
        default=False,
        nargs='?',
        const=True,
        help='Whether to add `from __future__ import annotations` '
             'to the top of a file, Should be true if adding this '
             'to a project running Python < 3.9',
    )
    args = parser.parse_args(argv)

    return_value = 0

    for filename in args.filenames:
        if fix_file(filename, args.futures):
            return_value = 1

    return return_value


if __name__ == '__main__':
    exit(main())
