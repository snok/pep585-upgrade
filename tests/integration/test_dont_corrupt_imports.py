"""Test for https://github.com/snok/pep585-upgrade/issues/12"""
from tests.integration import int_test

definition = '''
from typing import Any, Type, TypeVar

t: Type
'''

expected = '''
from typing import Any, TypeVar

t: type
'''


def test_format_function_definition():
    int_test(definition, expected)
    int_test(definition, expected, futures=True)
