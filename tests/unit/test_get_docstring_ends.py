import ast
from src.upgrade_type_hints.checker import get_docstring_ends
import textwrap
import pytest


test_data = [
    (
        textwrap.dedent(
            """
        \"""
        A multi-line
        doc string
        presented
        \"""
        from typing import List
        a: List[int] = [1, 2]
        """
        ),
        6,
    ),
    (
        textwrap.dedent(
            """
    #! /usr/bin/env python
    """
        ),
        -1,
    ),
    (
        textwrap.dedent(
            """
    import requests
    'is this docstring?'
    """
        ),
        -1,
    ),
]


@pytest.mark.parametrize("source,expected_position", test_data)
def test_get_docstring_ends(source, expected_position):
    tree = ast.parse(source)
    pos = get_docstring_ends(tree)
    assert pos == expected_position
