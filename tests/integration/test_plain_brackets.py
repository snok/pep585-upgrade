from tests.integration import int_test

example = """
from rest_framework.serializers import Serializer

x: [str, Serializer]
y: (str, str, ...)

def test(a: [([str], Serializer)], b: str = '') -> [str]:
    pass
"""

expected = """
from rest_framework.serializers import Serializer

x: [str, Serializer]
y: (str, str, ...)

def test(a: [([str], Serializer)], b: str = '') -> [str]:
    pass
"""


def test_bad_type_annotation_doesnt_flag_unhandled_ast_type():
    int_test(example, expected)
