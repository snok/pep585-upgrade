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
    Flattens a list of nested lists, and filters out falsy values.

    The list [1, 2, [3, [4, 5], None, 6], [7], 8]
     becomes [1, 2, 3, 4, 5, 6, 7, 8]
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


def get_imports_to_delete(new_imports: list[list], imports: dict) -> list[dict]:
    """
    Returns a list of typing imports to remove.
    """
    operations = []
    for _list in new_imports:
        for index, _import in enumerate(imports):
            for item in _list:
                if item['annotation'] in _import['names']:
                    operations.append(
                        {
                            'annotation': item['annotation'],
                            'line_start': _import['lineno'],
                            'line_stop': _import['end_lineno'],
                        }
                    )
                    imports[index]['names'].remove(item['annotation'])
                    continue
    return operations
