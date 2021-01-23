from tests.integration import int_test

example = """
from typing import Generator


x: Generator[str, str, None, None]
"""

expected = """
from collections.abc import Generator


x: Generator[str, str, None, None]
"""


def test_generator():
    int_test(example, expected, futures=True)
