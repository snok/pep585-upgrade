from tests.integration import int_test

example = """
from __future__ import annotations

from typing import List

x: List
"""

expected = """
from __future__ import annotations

x: list
"""


def test_no_duplicate_futures_annotations():
    """
    Originally forgot to check for existing futures imports before adding a new one.

    Creating this to avoid this in the future.
    """
    int_test(example, expected)
