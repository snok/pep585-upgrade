from tests.integration import int_test


def test_docstring_with_missing_future():
    example = '''
"""
A multi-line
docstring
"""

from typing import List

x: List
'''

    expected = '''
"""
A multi-line
docstring
"""

from __future__ import annotations

x: list
    '''
    int_test(example, expected, futures=True, expect_futures=False)
