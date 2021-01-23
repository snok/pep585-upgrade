from coverage.annotate import os

example = """from typing import List

from rest_framework.serializers import Serializer

def test(x: List[str]):
    pass
"""

_expected = """from rest_framework.serializers import Serializer

def test(x: list[str]):
    pass
"""

result_path = 'result.py'
expected_path = 'expected.py'


def test_remove_top_whitespace():
    """
    Makes sure we remove lines of pure whitespace at the top of a file.
    """
    with open(result_path, 'w+') as file:
        file.write(example)
    with open(expected_path, 'w+') as file:
        file.write(_expected)

    # Execute the pre-commit hook as a CLI
    os.system(f'poetry run upgrade-type-hints-script {result_path}')

    # Load the changed file
    with open(result_path, 'rb') as f:
        # we need to sort the lines, since the imports get added randomly atm
        result = f.readlines()

    with open(expected_path, 'rb') as f:
        expected = f.readlines()

    result = sorted(result)
    expected = sorted(expected)

    os.remove(result_path)
    os.remove(expected_path)

    for a, b in zip(result, expected):
        assert a == b, f'{a} != {b}'
