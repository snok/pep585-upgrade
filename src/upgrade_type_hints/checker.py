from __future__ import annotations

import ast
from typing import Union


class AnnotationFinder:
    def __init__(self, file: str) -> None:
        with open(file, 'rb') as file:
            content = file.read()
        self.tree = ast.parse(content)

    def run(self):
        objects = self.get_ast_objects(self.tree)

        annotation_list: list[dict[str, str]] = []
        for obj in objects:
            result = self.get_annotations(obj)
            if result:
                if isinstance(result, list):
                    annotation_list += result
                else:
                    annotation_list.append(result)

        return annotation_list

    @staticmethod
    def get_ast_objects(node: ast.Module):
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

    def get_annotations(self, node: ast.AST) -> Union[dict, list[dict]]:
        """
        Return all annotations contained in the received ast object.
        """
        if isinstance(node, ast.Str):
            return {
                'annotation': node.value,
                'line_number': node.lineno,
                'end_line_number': node.end_lineno,
                'column_offset': node.col_offset,
                'end_column_offset': node.end_col_offset,
            }
        elif isinstance(node, ast.Subscript):
            l = []
            if hasattr(node, 'slice'):
                l.append(self.get_annotations(node.slice))
            if hasattr(node, 'value'):
                l.append(self.get_annotations(node.value))
            if hasattr(node, 'id'):
                l.append(
                    {
                        'annotation': node.id,
                        'line_number': node.lineno,
                        'column_offset': node.col_offset,
                        'end_column_offset': node.end_col_offset,
                    }
                )
            if l:
                return list(self.flatten_list([i for i in l if i is not None]))
            else:
                print(f'Something went wrong: {node.__dict__}')
        elif isinstance(node, ast.Tuple):
            return [self.get_annotations(x) for x in node.elts]
        elif isinstance(node, ast.Name):
            return {
                'annotation': node.id,
                'line_number': node.lineno,
                'column_offset': node.col_offset,
                'end_column_offset': node.end_col_offset,
            }
        elif isinstance(node, ast.AnnAssign):
            annotation_node = node.annotation
            l = []
            if hasattr(annotation_node, 'slice'):
                l.append(self.get_annotations(annotation_node.slice))
            if hasattr(annotation_node, 'value'):
                l.append(self.get_annotations(annotation_node.value))
            if hasattr(annotation_node, 'id'):
                l.append(
                    {
                        'annotation': annotation_node.id,
                        'line_number': annotation_node.lineno,
                        'end_line_number': annotation_node.end_lineno,
                        'column_offset': annotation_node.col_offset,
                        'end_column_offset': annotation_node.end_col_offset,
                    }
                )
            if l:
                return list(self.flatten_list([i for i in l if i is not None]))
            else:
                print('Something went wrong')
        elif isinstance(node, ast.Attribute):
            if hasattr(node, 'name'):
                return self.get_annotations(node.name)
            else:
                return self.get_annotations(node.value)
        elif node is None or isinstance(node, ast.Constant) and node.value is None:
            return {}
        elif isinstance(node, str):
            # When imports are made inside a TYPE_CHECKING block, they will be
            # wrapped in str. Think we'll just avoid these for now, since they
            # don't have a line number, etc; otherwise we would be able to
            # change them pretty easily.
            return {}

        print(f'Unhandled: type {type(node)}, {node} ')
        return {}

    @staticmethod
    def flatten_list(alist):
        for item in alist:
            if isinstance(item, list):
                yield from item
            else:
                yield item
