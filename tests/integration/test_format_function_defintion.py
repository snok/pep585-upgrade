import os
import shutil

from tests import file_path

template_file = file_path / 'example_files/function_definition_template.py'
test_file = file_path / 'example_files/function_definition.py'
example_file = file_path / 'example_files/expected_function_definition.py'
project_dir = file_path.parent


def test_format_function_definition():
    # Set the file's content
    shutil.copyfile(template_file, test_file)

    # Execute the pre-commit hook as a CLI
    os.chdir(project_dir)
    os.system(f'poetry run upgrade_type_hints_script {test_file}')

    # Load the changed file
    with open(test_file, 'rb') as f:
        # we need to sort the lines, since the imports get added randomly atm
        result = sorted(f.readlines())
    with open(example_file, 'rb') as f:
        expected = sorted(f.readlines())

    for a, b in zip(result, expected):
        assert a == b
