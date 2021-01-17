from argparse import ArgumentTypeError

import pytest

from src.upgrade_type_hints.utils import str_to_bool


def test_str_to_bool():
    assert str_to_bool(True) is True
    assert str_to_bool(False) is False
    for x in ['yes', 'true', 't', 'y', '1']:
        assert str_to_bool(x) is True
    for x in ['no', 'false', 'f', 'n', '0']:
        assert str_to_bool(x) is False
    with pytest.raises(ArgumentTypeError):
        str_to_bool('bad argument')
