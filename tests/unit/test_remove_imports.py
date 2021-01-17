from src.upgrade_type_hints.update import remove_import


def test_same_line_import():
    content = [b'from typing import List']
    new_content = remove_import({'line_start': 1, 'line_stop': 1, 'annotation': 'List'}, content)
    assert new_content == []


def test_same_line_multiple_import():
    content = [b'from typing import List, Set, Dict, FrozenSet, Optional\n']
    for operation in [
        {'line_start': 1, 'line_stop': 1, 'annotation': 'List'},
        {'line_start': 1, 'line_stop': 1, 'annotation': 'Set'},
        {'line_start': 1, 'line_stop': 1, 'annotation': 'Dict'},
        {'line_start': 1, 'line_stop': 1, 'annotation': 'FrozenSet'},
    ]:
        content = remove_import(operation, content)
    assert content == [b'from typing import Optional\n']


def test_error_message(capsys):
    content = [b'from typing import List, Set, Dict, FrozenSet, Optional\n']
    for operation in [
        {'line_start': 1, 'line_stop': 1, 'annotation': 'Lists'},
    ]:
        content = remove_import(operation, content)
    captured = capsys.readouterr()
    assert (
        captured.out == 'Not able to find annotation Lists in file. '
        'Please report an issue to https://github.com/sondrelg/pep585-upgrade/issues\n'
    )
