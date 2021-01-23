from __future__ import annotations

import argparse
from collections.abc import Sequence
from typing import Optional

from .checker import find_annotations_and_imports_in_file
from .constants import NEEDS_FUTURES
from .definitions import check_if_types_need_substitution
from .update import update_file
from .utils import get_imports_to_delete, str_to_bool


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to run')
    parser.add_argument(
        '--futures',
        type=str_to_bool,
        default=False,
        nargs='?',
        const=True,
        help='Whether to add `from __future__ import annotations` '
        'to the top of a file, Set to true if using this in a project running Python < 3.9',
    )
    args = parser.parse_args(argv)
    futures: bool = args.futures or NEEDS_FUTURES

    return_value = 0

    for filename in args.filenames:
        # Fetch all typing imports and type annotations
        annotation_list, imports, futures_import_found = find_annotations_and_imports_in_file(filename)

        # Get all *relevant* type annotations (annotations we want to substitute)
        native_types, imported_types = check_if_types_need_substitution(annotation_list, imports)

        # Create a map of which imports to delete, wrt. substitutions
        imports_to_delete = get_imports_to_delete([native_types, imported_types], imports)

        if native_types or imported_types and imports_to_delete:
            print(f'Fixing {filename}')
            update_file(
                filename=filename,
                futures=futures,
                native_types=native_types,
                imported_types=imported_types,
                imports_to_delete=imports_to_delete,
                futures_import_found=futures_import_found,
            )
            return_value = 1

    return exit(return_value)
