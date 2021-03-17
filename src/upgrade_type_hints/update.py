from __future__ import annotations

import re


def replace_type(old_annotation: str, new_annotation: str, line) -> tuple[bytes, dict]:
    """
    Perform type replacement on a string (line).
    """
    new_annotation = bytes(new_annotation, encoding='utf-8')
    pattern = b'[^a-zA-Z](' + old_annotation.encode(encoding='utf-8') + b')(?:[^a-zA-Z]|$)'
    match = re.search(pattern, line)
    line = line[: match.start(1)] + line[match.end(1) :]
    line = line[: match.start(1)] + new_annotation + line[match.start(1) :]
    return line


def remove_import(operation, content):
    counter = 0

    for line in content[operation['line_start'] - 1 : operation['line_stop']]:
        # Check if this is the line the import is on
        if re.findall(f'[^a-zA-Z]{operation["annotation"]}(?:[^a-zA-Z]|$)'.encode(encoding='utf-8'), line):
            if operation['line_start'] == operation['line_stop']:
                # Handle same line imports here
                if b',' in line:
                    # example: from x import y, z
                    name = operation['annotation'].encode(encoding='utf-8')
                    match = re.search(
                        b'([^a-zA-Z]' + name + br'\s?,)|'  # `List,  `
                        br'(,\s?' + name + br'\s?)|'  # `, List`
                        br'(\s?' + name + br'\s?$)',
                        line,
                    )
                    if match:
                        groups = [i for i in match.groups() if i]
                        line = line.replace(groups[0].replace(b'\n', b''), b'', 1)
                    content[operation['line_start'] - 1] = line
                    break
                else:
                    # example: from x import y
                    # here we just remove the entire line from the file
                    del content[operation['line_start'] - 1]
                break

            # Handle multi-line imports
            content = (
                content[: operation['line_start'] - 1 + counter]
                + content[operation['line_start'] + counter :]
            )
            break

        counter += 1
    else:
        # The else block is triggered after the for-loop if it never hits a `break`
        print(
            f'Not able to find annotation {operation["annotation"]} in file. '
            'Please report an issue to '
            'https://github.com/sondrelg/pep585-upgrade/issues'
        )
    return content


def update_file(
    filename: str,
    futures: bool,
    native_types: list,
    imported_types: list,
    imports_to_delete: list,
    futures_import_found: bool,
) -> None:
    """
    Reads a file, removes imports and updates types, then writes back to it.
    """
    with open(filename, mode='rb+') as file:
        content = file.readlines()

    for item in native_types:
        # New native types don't require us to do anything except inplace-replacement of type hints
        content[item['line_number'] - 1] = replace_type(
            item['annotation'], item['new_annotation'], content[item['line_number'] - 1]
        )

    new_import_statements: list[bytes] = []
    for item in imported_types:
        # The types handled here require us to add a new import statement at
        # the top of the file in addition to the inplace replacement of type hints
        content[item['line_number'] - 1] = replace_type(
            item['annotation'], item['new_annotation'], content[item['line_number'] - 1]
        )
        new_import = f'from {item["import_from"]} import {item["new_annotation"]}\n'.encode(encoding='utf-8')
        if new_import not in content:
            new_import_statements.append(new_import)

    # Filter out repeated imports
    new_import_statements = list(set(new_import_statements))
    if futures and not futures_import_found:
        new_import_statements.insert(0, b'from __future__ import annotations\n\n')

    # Remove old imports
    for operation in imports_to_delete:
        content = remove_import(operation, content)

    content = new_import_statements + content
    with open(filename, 'wb') as file:
        file.writelines(content)
