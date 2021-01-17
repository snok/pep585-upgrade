import os


result_path = 'result.py'
expected_path = 'expected.py'


def int_test(function_definition, expected, futures=False):
    with open(result_path, 'w+') as file:
        file.write(function_definition)
    with open(expected_path, 'w+') as file:
        file.write(expected)

    # Execute the pre-commit hook as a CLI
    os.system(f'poetry run upgrade-type-hints-script {result_path}' + ' --futures=true' if futures else '')
    os.system(f'isort {result_path}')

    # Load the changed file
    with open(result_path, 'rb') as f:
        # we need to sort the lines, since the imports get added randomly atm
        result = f.readlines()

    with open(expected_path, 'rb') as f:
        expected = f.readlines() + [b'from __future__ import annotations\n'] if futures else []

    result = sorted(i for i in result if i.replace(b'\n', b''))
    expected = sorted(i for i in expected if i.replace(b'\n', b''))

    print(f'{result=}')

    os.remove(result_path)
    os.remove(expected_path)

    for a, b in zip(result, expected):
        assert a == b, f'{a} != {b}'
