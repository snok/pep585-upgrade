[![supported python versions](https://img.shields.io/badge/python-3.7%2B-blue)]()
[![code coverage](https://codecov.io/gh/sondrelg/pep585-upgrade/branch/master/graph/badge.svg?token=06RLJN3XNJ)](https://codecov.io/gh/sondrelg/pep585-upgrade)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

# PEP585 Upgrade

This is a [pre-commit](https://pre-commit.com/) hook configured to automatically upgrade your type hints
to the new native types implemented in [PEP 585](https://www.python.org/dev/peps/pep-0585/).

This will work for any Python version above `3.7`, though if you're not using `3.9` you will need to run the hook with `futures-imports=true`.

A complete type list is shown below.
<details>
<summary><b>See the complete list</b></summary>

<br>

| Used to be     	            | Will be upgraded to  	                                |
|---------------------------    |-------------------------------------------    |
| typing.Tuple     	            |  tuple     	                                |
| typing.List      	            |  list      	                                |
| typing.Dict      	            |  dict      	                                |
| typing.Set       	            |  set       	                                |
| typing.FrozenSet 	            |  frozenset 	                                |
| typing.Type      	            |  type      	                                |
| typing.Deque                  |  collections.deque                            |
| typing.DefaultDict            |  collections.defaultdict                      |
| typing.OrderedDict            |  collections.OrderedDict                      |
| typing.Counter                |  collections.Counter                          |
| typing.ChainMap               |  collections.ChainMap                         |
| typing.Awaitable              |  collections.abc.Awaitable                    |
| typing.Coroutine              |  collections.abc.Coroutine                    |
| typing.AsyncIterable          |  collections.abc.AsyncIterable                |
| typing.AsyncIterator          |  collections.abc.AsyncIterator                |
| typing.AsyncGenerator         |  collections.abc.AsyncGenerator               |
| typing.Iterable               |  collections.abc.Iterable                     |
| typing.Iterator               |  collections.abc.Iterator                     |
| typing.Generator              |  collections.abc.Generator                    |
| typing.Reversible             |  collections.abc.Reversible                   |
| typing.Container              |  collections.abc.Container                    |
| typing.Collection             |  collections.abc.Collection                   |
| typing.Callable               |  collections.abc.Callable                     |
| typing.AbstractSet            |  collections.abc.Set     |
| typing.MutableSet             |  collections.abc.MutableSet                   |
| typing.Mapping                |  collections.abc.Mapping                      |
| typing.MutableMapping         |  collections.abc.MutableMapping               |
| typing.Sequence               |  collections.abc.Sequence                     |
| typing.MutableSequence        |  collections.abc.MutableSequence              |
| typing.ByteString             |  collections.abc.ByteString                   |
| typing.MappingView            |  collections.abc.MappingView                  |
| typing.KeysView               |  collections.abc.KeysView                     |
| typing.ItemsView              |  collections.abc.ItemsView                    |
| typing.ValuesView             |  collections.abc.ValuesView                   |
| typing.ContextManager         |  contextlib.AbstractContextManager            |
| typing.AsyncContextManager    |  contextlib.AbstractAsyncContextManager       |
| typing.re.Pattern             |  re.Pattern                                   |
| typing.re.Match               |  re.Match                                     |

</details>

### I'm a visual learner

In a nutshell, this code

```python
from typing import List, Tuple, Dict, Set, FrozenSet

def do_thing(x: List[Tuple[str, ...]], y: Dict[str, Set[str]]) -> FrozenSet:
```

becomes this

```python
def do_thing(x: list[tuple[str, ...]], y: dict[str, set[str]]) -> frozenset:
```

or this, if you enable the futures option

```python
from __future__ import annotations

def do_thing(x: list[tuple[str, ...]], y: dict[str, set[str]]) -> frozenset:
```

### Features:
- [x] Performs in-line substitution for new types
- [x] Adds new imports for upgrade types which need them
- [x] Adds `__futures__` imports if the futures flag is enabled
- [x] Removes no longer needed typing imports

Note: even though we remove and add imports *reasonably* well, I would
recommend running this in tandem hook like `isort` to aggregate
and sort your imports, and flake8 to discover any unused imports neither were able to remove.
Otherwise you risk needing to do *some* manual cleanup
from time to time (though it should be pretty rare).

### Config

To use this with [pre-commit](https://pre-commit.com/), simply add this to your config file:

```yaml
- repo: https://github.com/sondrelg/pep585-upgrade
  rev: master  # or add a specific commit sha
  hooks:
  - id: upgrade-type-hints
    args: [ '--futures=true' ]
```

For more information about available arguments, see the [function definitions](https://github.com/sondrelg/pep585-upgrade/blob/master/src/upgrade_type_hints/update.py#L95).

### Running this once on my codebase

If you wish to run this once on your codebase, that's not easy to do *without* pre-commit, as it piggybacks on that process quite a bit.

However, installing pre-commit and configuring the hook to run will take you less than a minute. These are the steps:

- Run `pip install pre-commit`
- Run `touch pre-commit-config.yaml`
- Copy the configuration shown above into the file
- Run `pre-commit run --all-files`

### Running this once on a single file

To run the upgrade on a single file, you can clone the repo
and run `python -m upgrade_type_hints <filename>` from the src folder, or
something equivalent.

### Known imperfections

- We have a hard time removing common `import typing` imports, since we don't have a full inventory of all possible places `typing` could be used. Seeing something like this, you might think this is easy to handle

    ```python
    import typing

    x: typing.List
    ```

    but extending this example to a thousand-line file, the way we've structured the logic, there is no way to know whether there is a valid `typing.Optional` somewhere in the file.
- We might remove typing imports in a file where you needed them for more than just type annotations.
  An example of this is custom type declarations:

    ```python
    from typing import List

    x: List  # this will be upgraded and the import will be removed
    y = List[str]  # this will be left without its required import
    ```

  The reason for this is that custom type declarations are not a part
  of the `ast` objects we look at.

Both points are resolved by running flake8.

### Supporting the project

Please leave a ✭ if this project helped you 👏 and contributions are always welcome!
