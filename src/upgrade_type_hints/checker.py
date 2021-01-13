from __future__ import annotations

import ast
from typing import Union


def flatten_to_generator(_list: list):
    for item in _list:
        if isinstance(item, list):
            yield from item
        else:
            yield item


def flatten_list(_list: list) -> list:
    """
    Takes a list with possible nested lists and flattens the structure.
    """
    while True:
        for item in _list:
            if isinstance(item, list):
                _list = list(flatten_to_generator(_list))
                break
        else:
            return _list


def get_ast_objects(node: ast.Module) -> list[ast.AST]:
    """
    Returns all function arguments, function return values, and annotation objs.
    """
    items = []
    for item in ast.walk(node):
        if isinstance(item, ast.FunctionDef):
            for argument in item.args.args:
                if hasattr(argument, 'annotation'):
                    items.append(argument.annotation)
            if item.returns:
                items.append(item.returns)
        elif isinstance(item, ast.AnnAssign) and hasattr(item, 'annotation'):
            items.append(item)
    return items


def format_dict(annotation, d):
    return {
        'annotation': annotation,
        'line_number': d.lineno,
        'end_line_number': d.end_lineno,
        'column_offset': d.col_offset,
        'end_column_offset': d.end_col_offset,
    }


def get_annotations(node: ast.AST) -> Union[dict, list[dict]]:
    """
    Return all annotations contained in the received ast object.
    """
    if isinstance(node, ast.Str):
        return format_dict(node.value, node)
    elif isinstance(node, ast.Subscript):
        l = []
        if hasattr(node, 'slice'):
            l.append(get_annotations(node.slice))
        if hasattr(node, 'value'):
            l.append(get_annotations(node.value))
        if l:
            return flatten_list([i for i in l if i is not None])
    elif isinstance(node, ast.Tuple):
        return [get_annotations(x) for x in node.elts]
    elif isinstance(node, ast.Name):
        return format_dict(node.id, node)
    elif isinstance(node, ast.AnnAssign):
        l = []
        annotation_node = node.annotation
        if hasattr(annotation_node, 'slice'):
            l.append(get_annotations(annotation_node.slice))
        if hasattr(annotation_node, 'value'):
            if isinstance(annotation_node.value, str):
                l.append(format_dict(annotation_node.value, annotation_node))
            else:
                l.append(get_annotations(annotation_node.value))
        if hasattr(annotation_node, 'id'):
            l.append(format_dict(annotation_node.id, annotation_node))
        if l:
            return flatten_list([i for i in l if i is not None])
    elif isinstance(node, ast.Attribute):
        # This probably isn't really how to handle attribute nodes,
        # but it is important that we save a typing.Dict annotation
        # in a way where we can substitute the annotation later.
        # See the test_ast_attribute test for insight on how this works.
        return format_dict(f'{node.value.id}.{node.attr}', node)
    elif node is None or isinstance(node, ast.Constant) and node.value is None:
        return {}

    raise Exception(f'Something went wrong: {node.__dict__}')


def find_annotations_in_file(file: str) -> list[dict[str, str]]:
    with open(file, 'rb') as file:
        content = file.read()

    objects = get_ast_objects(ast.parse(content))

    annotation_list: list[dict[str, str]] = []
    for obj in objects:
        result = get_annotations(obj)
        if result:
            if isinstance(result, list):
                annotation_list += result
            else:
                annotation_list.append(result)

    return annotation_list
