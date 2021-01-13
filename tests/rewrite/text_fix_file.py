# import pathlib
# from shutil import copyfile
#
# from src.upgrade_type_hints import fix_file
#
# path = pathlib.Path(__file__).parent.absolute()
#
#
# def test_fix_file():
#     # Create a new copy of the test-example file
#     example_file = path / 'typing_example.py'
#     temp_path = path / 'test_file.py'
#     copyfile(example_file, temp_path)
#     assert fix_file(temp_path, futures=True)
