from __future__ import annotations

import argparse
from typing import Optional, Sequence

from .checker import AnnotationFinder
from .definitions import check_if_types_need_substitution
from .utils import str_to_bool

#
# def process_line(line: bytes) -> tuple[bytes, set[tuple[bytes, bytes]], bool]:
#     """
#     Finds replacement candidates.
#
#     :return: List of matches, where each match is represented by a set
#             containing:
#         - A set containing the starting and ending index of the candidate
#         - The old name
#         - The name of the new type it should be replaced with
#         - The import that has to be made at the top level
#     """
#     upgraded = False
#     imports = set()
#     for m in re.finditer(native_type_pattern, line):
#         match = line[m.start(0): m.end(0)].replace(b'typing.', b'')
#         old_type = clean(match)
#         new_type = native_types[old_type.decode()].encode('utf-8')
#         new_val = match.replace(old_type, new_type)
#         line = line[: m.start(0)] + new_val + line[m.end(0):]
#         upgraded = True
#     for m in re.finditer(imported_type_pattern, line):
#         match = line[m.start(0): m.end(0)].replace(b'typing.', b'')
#         old_type = clean(match)
#         new_obj = imported_types[old_type.decode()]
#         new_type = new_obj['name'].encode('utf-8')
#         new_val = match.replace(old_type, new_type)
#         line = line[: m.start(0)] + new_val + line[m.end(0):]
#         upgraded = True
#         imports.add((new_obj['from'].encode('utf-8'), new_type))
#
#     return line, imports, upgraded


def replace_type(item: dict, line) -> bytes:
    col_offset = item['column_offset']
    end_col_offset = item['end_column_offset']
    new_annotation = bytes(item['new_annotation'], encoding='utf-8')
    print(f'The original value is: {line}')
    line = line[:col_offset] + line[end_col_offset:]
    line = line[:col_offset] + new_annotation + line[col_offset:]
    print(f'The new value is {line}\n')
    return line


def fix_file(filename: str, futures: bool, native: list, unique_import: list, repeat_import: list) -> bool:
    """
    Writes changes to a file.
    """
    with open(filename, mode='rb+') as file:
        # Read the file
        content = file.readlines()

    # for item in native:
    #     content[item['line_number'] - 1] = replace_type(item, content[
    #         item['line_number'] - 1])

    new_import_statements: list[bytes] = []

    for item in unique_import:
        print('\n', item)
        content[item['line_number'] - 1] = replace_type(item, content[item['line_number'] - 1])
        new_import_statements.append(
            b'from '
            + bytes(item['import_from'], encoding='utf-8')
            + b' import '
            + bytes(item['new_annotation'], encoding='utf-8')
            + b'\n'
        )
        #
        #     for line_no, line in enumerate(content):
        #
        #         # Fetch upgrade candidates for individual lines
        #         line, imports, upgraded = process_line(line)
        #
        #         if upgraded:
        #             any_file_upgraded = True
        #             file_upgraded = True
        #             content[line_no] = line
        #             if imports:
        #                 unique_imports.update(imports)
        #
        #     if file_upgraded:
        #         # Only need to print once per file, so move this out
        #         print(f'Upgrading types in {filename}')
        #
        #     concat_imports = list(
        # {
        #          in unique_imports}
        #     )
        #     if futures:
        #         concat_imports = [
        #                              b'from __future__ import annotations\n\n'] + concat_imports
        new_import_statements = list({i for i in new_import_statements})
        content = new_import_statements + content
        # with open(filename, 'wb') as file:
        #     file.writelines(content)  # + concat_imports


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
        annotations = AnnotationFinder(filename).run()
        native, unique_import, repeat_import = check_if_types_need_substitution(annotations)
        if native or unique_import or repeat_import:
            fix_file(filename, args.futures, native, unique_import, repeat_import)
            return_value = 1

    return return_value
