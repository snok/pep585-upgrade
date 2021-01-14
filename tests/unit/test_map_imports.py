import ast

from src.upgrade_type_hints.checker import map_imports


def test_map_imports():
    """
    Make sure we're able to discover all imports.
    """
    code_example = 'from x import y'
    tree = ast.parse(code_example)
    imports = map_imports(tree)
    assert imports == {'lineno': 1, 'end_lineno': 1, 'names': {'y'}}

    code_example = 'from x import y, z'
    tree = ast.parse(code_example)
    imports = map_imports(tree)
    assert imports == {'lineno': 1, 'end_lineno': 1, 'names': {'y', 'z'}}

    code_example = 'from x import (\n\ty,\n\tz\n\t)'
    tree = ast.parse(code_example)
    imports = map_imports(tree)
    assert imports == {'lineno': 1, 'end_lineno': 4, 'names': {'y', 'z'}}

    code_example = 'from \\\n\tx import (\n\ty,\n\tz\n\t); from x\\\n\t import zz'
    tree = ast.parse(code_example)
    imports = map_imports(tree)
    assert imports == {'end_lineno': 6, 'lineno': 5, 'names': {'y', 'zz', 'z'}}
