import ast

from src.upgrade_type_hints.checker import map_imports


def test_map_imports():
    """
    Make sure we're able to discover all typing imports.
    """
    code_example = 'from typing import List'
    tree = ast.parse(code_example)
    imports = map_imports(tree)
    assert imports == [{'lineno': 1, 'end_lineno': 1, 'names': {'List'}}]

    code_example = 'from typing import List, Dict'
    tree = ast.parse(code_example)
    imports = map_imports(tree)
    assert imports == [{'lineno': 1, 'end_lineno': 1, 'names': {'List', 'Dict'}}]

    code_example = 'from typing import (\n\tList,\n\tDict\n\t)'
    tree = ast.parse(code_example)
    imports = map_imports(tree)
    assert imports == [{'lineno': 1, 'end_lineno': 4, 'names': {'List', 'Dict'}}]

    code_example = 'from \\\n\ttyping import (\n\tList,\n\tDict\n\t); from typing\\\n\t import Set'
    tree = ast.parse(code_example)
    imports = map_imports(tree)
    assert imports == [
        {'end_lineno': 5, 'lineno': 1, 'names': {'Dict', 'List'}},
        {'end_lineno': 6, 'lineno': 5, 'names': {'Set'}},
    ]

    code_example = 'from \\\n\ttyping import (\n\tList,\n\tDict\n\t); from x\\\n\t import Set'
    tree = ast.parse(code_example)
    imports = map_imports(tree)
    assert imports == [{'end_lineno': 5, 'lineno': 1, 'names': {'Dict', 'List'}}]


def test_map_non_typing_imports():
    """
    No non-typing imports should be mapped.
    """
    code_example = 'from x import List'
    tree = ast.parse(code_example)
    imports = map_imports(tree)
    assert imports == []
