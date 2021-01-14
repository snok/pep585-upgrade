import ast

from src.upgrade_type_hints.checker import map_imports


def test_map_from_imports():
    """
    These are not really tests. Just a slow exploration
    of how the import objects look like. Might want
    to remove them in the future.
    """
    code_example = 'from x import y'
    tree = ast.parse(code_example)
    direct, _from = map_imports(tree)
    assert len(_from) == 1
    assert len(_from[0].names) == 1
    assert _from[0].module == 'x'
    assert _from[0].names[0].name == 'y'

    code_example = 'from x import y, z'
    tree = ast.parse(code_example)
    direct, _from = map_imports(tree)
    assert len(_from) == 1
    assert len(_from[0].names) == 2
    assert _from[0].module == 'x'
    assert _from[0].names[0].name == 'y'
    assert _from[0].names[1].name == 'z'

    code_example = 'from x import (\n\ty,\n\tz\n\t)'
    tree = ast.parse(code_example)
    direct, _from = map_imports(tree)
    assert len(_from) == 1
    assert len(_from[0].names) == 2
    assert _from[0].module == 'x'
    assert _from[0].names[0].name == 'y'
    assert _from[0].names[1].name == 'z'
    assert _from[0].lineno == 1
    assert _from[0].end_lineno == 4

    # TODO:
    # Map out this way:
    # When we need to delete an import just check if names
    # is greater than one. If > 1: find the line in the
    # lineno span and delete it, then delete that name from
    # the dict and reduce the lineno span by 1 line.
    # if it is exactly one, delete all lines (1-3) and
    # remove the key altogether.
    x = [
        {
            item.module: {
                'names': [i.name for i in item.names],
                'lineno': item.lineno,
                'end_lineno': item.end_lineno,
            }
        }
        for item in _from
    ]
    assert 2 == 3


def test_map_imports():
    code_example = 'import x,\\\n\ty'
    tree = ast.parse(code_example)
    direct, _ = map_imports(tree)
    x = [
        {'names': [i.name for i in item.names], 'lineno': item.lineno, 'end_lineno': item.end_lineno}
        for item in direct
    ]
    assert x == [{'names': ['x', 'y'], 'lineno': 1, 'end_lineno': 2}]
