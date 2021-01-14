import os
import shutil

from tests import file_path


def test_format_function_definition():
    # Set the file's content
    shutil.copyfile(
        file_path / 'example_files/function_definition_template.py',
        file_path / 'example_files/function_definition.py',
    )

    # Execute the pre-commit hook as a CLI
    os.chdir(file_path.parent)
    os.system(f'poetry run upgrade_type_hints_script {file_path / "example_files/function_definition.py"}')

    # Load the changed file
    with open('tests/example_files/function_definition.py', 'rb') as f:
        # we need to sort the lines, since the imports get added randomly atm
        result = sorted(f.readlines())
    with open('tests/example_files/expected_function_definition.py', 'rb') as f:
        expected = sorted(f.readlines())

    for a, b in zip(result, expected):
        assert a == b
