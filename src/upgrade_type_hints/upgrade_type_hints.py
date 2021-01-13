from __future__ import annotations

import argparse
from typing import Optional, Sequence

from .checker import find_annotations_in_file
from .definitions import check_if_types_need_substitution
from .utils import str_to_bool


def replace_type(item: dict, line) -> bytes:
    col_offset = item['column_offset']
    end_col_offset = item['end_column_offset']
    new_annotation = bytes(item['new_annotation'], encoding='utf-8')
    line = line[:col_offset] + line[end_col_offset:]
    line = line[:col_offset] + new_annotation + line[col_offset:]
    return line


def fix_file(filename: str, futures: bool, native: list, unique_import: list, repeat_import: list) -> None:
    """
    Writes changes to a file.
    """
    with open(filename, mode='rb+') as file:
        content = file.readlines()

    imports_to_remove = []

    for item in native:
        content[item['line_number'] - 1] = replace_type(item, content[item['line_number'] - 1])
        imports_to_remove.append(item['annotation'])

    new_import_statements: list[bytes] = []

    for item in unique_import:
        content[item['line_number'] - 1] = replace_type(item, content[item['line_number'] - 1])
        new_import_statements.append(
            f'from {item["import_from"]} import {item["new_annotation"]}\n'.encode(encoding='utf-8')
        )
        imports_to_remove.append(item['annotation'])

    for item in repeat_import:
        # Since the annotation is the same, we just need to add the correct import
        new_import_statements.append(
            f'from {item["import_from"]} import {item["new_annotation"]}\n'.encode(encoding='utf-8')
        )
        imports_to_remove.append(item['annotation'])

    # Make sure we only add unique imports
    new_import_statements = list(set(new_import_statements))
    if futures:
        new_import_statements.insert(0, b'from __future__ import annotations\n\n')

    # Remove old imports
    imports_to_remove = ['typing.' + i for i in imports_to_remove]
    for _import in imports_to_remove:
        # TODO: remove imports
        pass

    content = new_import_statements + content
    with open(filename, 'wb') as file:
        file.writelines(content)


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
        annotation_list = find_annotations_in_file(filename)
        native, unique_import, repeat_import = check_if_types_need_substitution(annotation_list)
        if native or unique_import or repeat_import:
            fix_file(filename, args.futures, native, unique_import, repeat_import)
            return_value = 1

    return return_value
