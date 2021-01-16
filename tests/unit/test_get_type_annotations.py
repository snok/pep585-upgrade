import ast
import textwrap

from src.upgrade_type_hints.checker import flatten_list, get_annotations, get_ast_objects


class TestAst:
    def test_get_ast_objects(self):
        example_code = textwrap.dedent(
            """
            a: dict = {}

            def test(x: int, y: str) -> None:
                pass

            """
        )

        """
        From the example code we've set up above, we expect to receive 4 useful objects:

            - The `a: dict` annotation assignment (ast.AnnAssign type)
            - The `x: int` argument (ast.Name type)
            - The `y: str` argument (ast.Name type)
            - The `-> None` return value (ast.Constant type)

        If we don't, our hook wouldn't work. We also expect them in this order.
        """

        tree = ast.parse(example_code)
        objects = get_ast_objects(tree)

        assert type(objects[0]) == ast.AnnAssign and objects[0].annotation.id == 'dict'
        assert type(objects[1]) == ast.Name and objects[1].id == 'int'
        assert type(objects[2]) == ast.Name and objects[2].id == 'str'
        assert type(objects[3]) == ast.Constant and objects[3].value is None

        """
        Since we know the annotations we're expecting here, we can also quickly
        add another sub-test.
        """

        annotations = flatten_list([get_annotations(obj) for obj in objects])

        assert annotations[0]['annotation'] == 'dict'
        assert annotations[1]['annotation'] == 'int'
        assert annotations[2]['annotation'] == 'str'
        assert len(annotations) == 3

    def test_get_complex_variable_annotation(self):
        example_code = 'a: Dict[Dict[Pattern, MutableSet], Tuple[Optional[str], Sequence]] = {}'
        tree = ast.parse(example_code)
        objects = get_ast_objects(tree)
        annotations = flatten_list([get_annotations(obj) for obj in objects])
        just_annotations = [i['annotation'] for i in annotations]
        assert just_annotations.count('Dict') == 2
        assert just_annotations.count('Tuple') == 1
        assert just_annotations.count('str') == 1
        assert just_annotations.count('Sequence') == 1
        assert just_annotations.count('Pattern') == 1
        assert just_annotations.count('MutableSet') == 1

    def test_quoted_ast_annassign(self):
        example_code = "a: 'DjangoModel'"
        tree = ast.parse(example_code)
        objects = get_ast_objects(tree)
        assert type(objects[0]) == ast.AnnAssign
        annotations = flatten_list([get_annotations(obj) for obj in objects])
        assert annotations[0]['annotation'] == 'DjangoModel'

    def test_ast_name(self):
        example_code = 'def test() -> DjangoModel:\n' '    pass'
        tree = ast.parse(example_code)
        objects = get_ast_objects(tree)
        assert type(objects[0]) == ast.Name
        annotations = flatten_list([get_annotations(obj) for obj in objects])
        assert annotations[0]['annotation'] == 'DjangoModel'

    def test_ast_subscript(self):
        example_code = "def test() -> Literal['one', 'two', 'three']:\n" '    pass'
        tree = ast.parse(example_code)
        objects = get_ast_objects(tree)
        assert type(objects[0]) == ast.Subscript
        annotations = flatten_list([get_annotations(obj) for obj in objects])
        assert annotations[0]['annotation'] == 'one'
        assert annotations[1]['annotation'] == 'two'
        assert annotations[2]['annotation'] == 'three'
        assert annotations[3]['annotation'] == 'Literal'

    def test_ast_tuple(self):
        example_code = "def test() -> Literal['one', 'two', 'three']:\n" '    pass'
        tree = ast.parse(example_code)
        objects = get_ast_objects(tree)
        tuple_object = objects[0].slice
        assert type(tuple_object) == ast.Tuple
        annotations = flatten_list([get_annotations(obj) for obj in objects])
        assert annotations[0]['annotation'] == 'one'
        assert annotations[1]['annotation'] == 'two'
        assert annotations[2]['annotation'] == 'three'
        assert annotations[3]['annotation'] == 'Literal'
        assert len(annotations) == 4

    def test_ast_attribute(self):
        example_code = 'variable: typing.Dict[typing.Dict[typing.Tuple[dict, list], str], int]'
        tree = ast.parse(example_code)
        objects = get_ast_objects(tree)
        annotations = flatten_list([get_annotations(obj) for obj in objects])
        just_annotations = [i['annotation'] for i in annotations]
        assert just_annotations.count('typing.Dict') == 2
        assert just_annotations.count('typing.Tuple') == 1
        assert just_annotations.count('dict') == 1
        assert just_annotations.count('list') == 1
        assert just_annotations.count('str') == 1
        assert just_annotations.count('int') == 1

    def test_simple_typing_import(self):
        example_code = 'import typing\n\nx: typing.List'
        tree = ast.parse(example_code)
        objects = get_ast_objects(tree)
        annotations = flatten_list([get_annotations(obj) for obj in objects])
        just_annotations = [i['annotation'] for i in annotations]
        assert just_annotations == ['typing.List']

    def test_custom_type(self):
        example_code = 'x = Tuple[float, float, float]'
        tree = ast.parse(example_code)
        objects = get_ast_objects(tree)
        annotations = flatten_list([get_annotations(obj) for obj in objects])
        just_annotations = [i['annotation'] for i in annotations]
        assert just_annotations == []

    def test_star_import(self):
        example_code = textwrap.dedent(
            '''
            from typing import List

            x: List


            def b(*, x: List[str]):
                pass
        '''
        )
        tree = ast.parse(example_code)
        objects = get_ast_objects(tree)
        annotations = flatten_list([get_annotations(obj) for obj in objects])
        assert annotations == [
            {'annotation': 'List', 'line_number': 4},
            {'annotation': 'str', 'line_number': 7},
            {'annotation': 'List', 'line_number': 7},
        ]
