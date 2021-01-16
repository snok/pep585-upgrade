from src.upgrade_type_hints.checker import flatten_list


class FlattenListTest:
    def test_flatten_list(self):
        x = [1, 2, [3, [4, 5], None, 6], [7], 8]
        assert flatten_list(x) == [1, 2, 3, 4, 5, 6, 7, 8]

    def test_flatten_another_list(self):
        x = [
            [
                {'a': 'str'},
                [[{'a': 'str'}, {'a': 'Optional'}], {'a': 'Sequence'}, {'a': 'Tuple'}],
                {
                    'a': 'Dict',
                },
            ]
        ]
        assert flatten_list(x) == [
            {'a': 'str'},
            {'a': 'str'},
            {'a': 'Optional'},
            {'a': 'Sequence'},
            {'a': 'Tuple'},
            {'a': 'Dict'},
        ]
