import os
import shutil

from tests import file_path


def test_format_function_definition():
    # Set the file's content
    shutil.copyfile(
        'tests/example_files/function_definition_template.py',
        'tests/example_files/function_definition.py',
    )

    # Execute the pre-commit hook as a CLI
    os.chdir(file_path.parent / 'src')
    os.system(
        f'python -m upgrade_type_hints {file_path.parent / "tests/example_files/function_definition.py"}'
    )

    # Load the changed file

    with open('../tests/example_files/function_definition.py', 'rb') as f:
        # we need to sort the lines, since the imports get added randomly atm
        result = sorted(f.readlines())
    with open('../tests/example_files/expected_function_definition.py', 'rb') as f:
        expected = sorted(f.readlines())

    for a, b in zip(result, expected):
        assert a == b
