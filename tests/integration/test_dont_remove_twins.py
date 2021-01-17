from tests.integration import int_test

definition = '''
from . import Type
from typing import (
    List,
)


def func(a: List) -> Type:
    pass
'''

expectd = '''
from . import Type


def func(a: list) -> Type:
    pass
'''


def test_format_function_definition():
    int_test(definition, expectd)
    int_test(definition, expectd, futures=True)
