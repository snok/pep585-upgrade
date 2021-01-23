from tests.integration import int_test

example = """
y: (str, ...)

def test(a: ([], )):
    print(a)
"""

expected = """
y: (str, ...)

def test(a: ([], )):
    print(a)
"""


def test_bad_type_annotation_doesnt_flag_unhandled_ast_type():
    int_test(example, expected)
