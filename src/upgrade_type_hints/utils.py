import argparse


def str_to_bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def flatten_to_generator(_list: list):
    for item in _list:
        if isinstance(item, list):
            yield from item
        else:
            yield item


def flatten_list(_list: list) -> list:
    """
    Flattens a list of nested lists.
    """
    while True:
        for index, item in enumerate(_list):
            if not item:
                _list.pop(index)
            if isinstance(item, list):
                _list = list(flatten_to_generator(_list))
                break
        else:
            return _list
