from __future__ import annotations

import argparse
import re
from typing import Optional, Sequence

from .checker import find_annotations_and_imports_in_file
from .definitions import check_if_types_need_substitution
from .utils import str_to_bool


def replace_type(item: dict, line) -> tuple[bytes, dict]:
    """
    Perform the type replacement for a line.
    """
    new_annotation = bytes(item['new_annotation'], encoding='utf-8')
    pattern = b'[^a-zA-Z](' + item['annotation'].encode(encoding='utf-8') + b')[^a-zA-Z]'
    match = re.search(pattern, line)
    print(f'Removing {line[match.start(1):match.end(1)]} and inserting {new_annotation}')
    line = line[: match.start(1)] + line[match.end(1) :]
    line = line[: match.start(1)] + new_annotation + line[match.start(1) :]
    return line


def fix_file(
    filename: str, futures: bool, native_types: list, imported_types: list, imports_to_delete: list
) -> None:
    """
    Changes the file's content and writes back to it.
    """
    with open(filename, mode='rb+') as file:
        content = file.readlines()

    for item in native_types:
        # New native types don't require us to do anything except
        # inplace replace the old values with the new
        content[item['line_number'] - 1] = replace_type(item, content[item['line_number'] - 1])

    new_import_statements: list[bytes] = []

    for item in imported_types:
        # These types require us to add a new import statement at the top of
        # the file in addition to the inplace replacement
        content[item['line_number'] - 1] = replace_type(item, content[item['line_number'] - 1])
        new_import_statements.append(
            f'from {item["import_from"]} import {item["new_annotation"]}\n'.encode(encoding='utf-8')
        )

    # Filter out repeated imports
    new_import_statements = list(set(new_import_statements))
    if futures:
        new_import_statements.insert(0, b'from __future__ import annotations\n\n')

    # Remove old imports
    for operation in imports_to_delete:
        ann, start, stop = operation['annotation'], operation['line_start'], operation['line_stop']
        counter = 0
        for line in content[start:stop]:
            if re.findall(f'[^a-zA-Z]{ann}[^a-zA-Z]'.encode(encoding='utf-8'), line):
                content = content[: start + counter] + content[start + counter + 1 :]
                break
            counter += 1
        else:
            Exception(f'Unable to find {ann}')

    content = new_import_statements + content
    with open(filename, 'wb') as file:
        file.writelines(content)


def map_imports_to_delete(new_imports: list[list], imports: dict):
    """
    This function handles creating a list of executable operations for deleting
    typing imports from the file we're handling.
    """
    operations = []
    counter = 0
    for _list in new_imports:
        for item in _list:
            if item['annotation'] in imports['names']:
                operations.append(
                    {
                        'annotation': item['annotation'],
                        'line_start': imports['lineno'],
                        'line_stop': imports['end_lineno'],
                    }
                )
                imports['end_lineno'] -= 1
                imports['names'].remove(item['annotation'])
                counter += 1
                continue
    return operations


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

    import shutil

    shutil.copyfile(
        '/Users/sondrelg/Documents/pep585-upgrade/tests/example_files/function_definition_template.py',
        '/Users/sondrelg/Documents/pep585-upgrade/tests/example_files/function_definition.py',
    )

    return_value = 0

    for filename in args.filenames:

        annotation_list, imports = find_annotations_and_imports_in_file(filename)
        native_types, imported_types = check_if_types_need_substitution(annotation_list)
        imports_to_delete = map_imports_to_delete([native_types, imported_types], imports)
        if native_types or imported_types:
            fix_file(filename, args.futures, native_types, imported_types, imports_to_delete)
            return_value = 1

    return return_value
