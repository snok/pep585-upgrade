# from src.upgrade_type_hints import process_line
#
#
# def test_comment_without_kwarg():
#     lines = [
#         {
#             'original': b'def test(x: int, y: Optional[List[str]]) -> Set[Dict[Tuple[str, str]]]:\r\n',
#             'expected': b'def test(x: int, y: Optional[list[str]]) -> set[dict[tuple[str, str]]]:\r\n',
#             'import': set(),
#         },
#         {
#             'original': b'def test(x: typing.FrozenSet) -> None:\r\n',
#             'expected': b'def test(x: frozenset) -> None:\r\n',
#             'import': set(),
#         },
#         {
#             'original': b'def test(x: typing.Counter) -> None:\r\n',
#             'expected': b'def test(x: Counter) -> None:\r\n',
#             'import': {
#                 (b'collections', b'Counter'),
#             },
#         },
#     ]
#     for d in lines:
#         original, expected, expected_imports = d['original'], d['expected'], d['import']
#         line, imports, upgraded = process_line(original)
#         assert line == expected
#         assert imports == expected_imports
