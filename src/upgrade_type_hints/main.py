from __future__ import annotations

import argparse
from collections.abc import Sequence
from typing import Optional

from .checker import find_annotations_and_imports_in_file
from .definitions import check_if_types_need_substitution
from .update import fix_file, map_imports_to_delete
from .utils import str_to_bool


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

        annotation_list, imports = find_annotations_and_imports_in_file(filename)
        native_types, imported_types = check_if_types_need_substitution(annotation_list)
        imports_to_delete = map_imports_to_delete([native_types, imported_types], imports)
        if native_types or imported_types:
            print(f'Upgrading types in {filename}')
            fix_file(filename, args.futures, native_types, imported_types, imports_to_delete)
            return_value = 1

    return exit(return_value)
