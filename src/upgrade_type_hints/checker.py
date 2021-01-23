from __future__ import annotations

import ast
from typing import Union

import _ast

from .constants import NEEDS_FUTURES
from .utils import flatten_list


def get_ast_objects(node: ast.Module) -> list[ast.AST]:
    """
    Returns all function arguments, function return values, and pure annotation objects.
    """
    items = []
    for item in ast.walk(node):
        if isinstance(item, ast.FunctionDef):
            for argument in item.args.args + item.args.kwonlyargs:
                if hasattr(argument, 'annotation'):
                    items.append(argument.annotation)
            if item.returns:
                items.append(item.returns)
        elif isinstance(item, ast.AnnAssign) and hasattr(item, 'annotation'):
            items.append(item)
    return items


def get_annotations(node: ast.AST) -> Union[dict, list[dict]]:  # noqa: C901
    """
    Return all annotations contained in the received ast object.
    """
    if isinstance(node, ast.Str):
        return {'annotation': node.value, 'line_number': node.lineno}

    elif isinstance(node, ast.Subscript):
        sublist = []
        if hasattr(node, 'slice'):
            sublist.append(get_annotations(node.slice))
        if hasattr(node, 'value'):
            sublist.append(get_annotations(node.value))
        if sublist:
            return flatten_list(sublist)

    elif isinstance(node, (ast.Tuple, ast.List)):
        return [get_annotations(x) for x in node.elts]

    elif isinstance(node, ast.Name):
        return {'annotation': node.id, 'line_number': node.lineno}

    elif isinstance(node, ast.AnnAssign):
        annotation_node = node.annotation

        if isinstance(annotation_node, ast.Attribute):
            # example: typing.List
            return get_annotations(annotation_node)

        sublist = []
        if hasattr(annotation_node, 'slice'):
            sublist.append(get_annotations(annotation_node.slice))
        if hasattr(annotation_node, 'value'):
            if isinstance(annotation_node.value, str):
                sublist.append({'annotation': annotation_node.value, 'line_number': annotation_node.lineno})
            else:
                sublist.append(get_annotations(annotation_node.value))
        if hasattr(annotation_node, 'id'):
            sublist.append({'annotation': annotation_node.id, 'line_number': annotation_node.lineno})
        if sublist:
            return flatten_list(sublist)

    elif isinstance(node, ast.Attribute):
        # Imports like typing.Dict are several layers deep, but we want to save
        # them to our annotation map as a single type so we can replace them
        # more easily.
        try:
            return {'annotation': f'{node.value.id}.{node.attr}', 'line_number': node.lineno}
        except AttributeError:
            # Types like pd.core.frame.DataFrame will throw AttributeErrors, but
            # we're only after relevant typing imports, which all have a max depth of 2
            return {}

    elif node is None or isinstance(node, ast.Constant):
        # We don't care about these
        return {}

    if NEEDS_FUTURES and isinstance(node, _ast.Index):
        sublist = []
        if hasattr(node, 'value') and not isinstance(node.value, str):
            sublist.append(get_annotations(node.value))
        if sublist:
            return flatten_list(sublist)

    print(
        'Found an unhandled ast object. '
        'Please report an issue to '
        'https://github.com/sondrelg/pep585-upgrade/issues'
    )


def map_imports(tree: ast.Module) -> tuple[list, bool]:
    """
    This function finds all typing imports.
    """
    imports = {}
    futures_import_found = False
    for item in tree.body:
        if isinstance(item, (ast.Import, ast.ImportFrom)):
            if not futures_import_found and isinstance(item, ast.ImportFrom) and item.module == '__future__':
                for i in item.names:
                    if i.name == 'annotations':
                        futures_import_found = True
            if isinstance(item, ast.ImportFrom) and item.module != 'typing':
                continue
            elif isinstance(item, ast.Import) and not any(i.name != 'typing' for i in item.names):
                continue
            if item.lineno not in imports:
                imports[item.lineno] = {'lineno': None, 'end_lineno': None, 'names': set()}
            imports[item.lineno]['lineno'] = item.lineno
            imports[item.lineno]['end_lineno'] = item.end_lineno
            for name in item.names:
                imports[item.lineno]['names'].add(name.name)

    return list(imports.values()), futures_import_found


def find_annotations_and_imports_in_file(file: str) -> tuple[list[dict[str, str]], list[dict], bool]:
    """
    Returns a complete map of typing imports and annotations in a given file.
    """
    with open(file, 'rb') as file:
        content = file.read()

    tree = ast.parse(content)
    imports, futures_import_found = map_imports(tree)
    objects = get_ast_objects(tree)

    annotation_list: list[dict[str, str]] = []
    for obj in objects:
        result = get_annotations(obj)
        if result:
            if isinstance(result, list):
                annotation_list += result
            else:
                annotation_list.append(result)

    return flatten_list(annotation_list), imports, futures_import_found
