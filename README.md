> Work in progress

# PEP585 Upgrade

This is a [pre-commit](https://pre-commit.com/) hook configured to automatically upgrade your type hints
to the new native types implemented in [PEP 585](https://www.python.org/dev/peps/pep-0585/).

They are available with any Python version above `3.7`, but if you're below `3.9` you will need to run it with `futures-imports=true`.

A complete list of the newly introduced types are shown below.
<details>
<summary><b>See the complete list of new types</b></summary>

<br>

| Used to be     	            | Was upgraded to  	                                |
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

### Show me

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
- [x] Perform in-line substitution for new types
- [x] Add required imports for non-builtin types, when they are replaced in
- [x] Add `__futures__` imports if enabled
- [x] Remove the (now unused) typing imports
- [ ] ~~More complex import handling, sorting, and removal~~

As a small aside; since thorough import handling isn't in the scope of this package,
we would recommend running this in tandem with a hook like `isort` to aggregate
and sort your imports. Otherwise you risk needing to do *some* manual cleanup
from time to time (though it should be pretty rare).

### Config

To use this with [pre-commit](https://pre-commit.com/), simply add this to your config file:

```yaml
- repo: https://github.com/sondrelg/pep585-upgrade
  rev: master  # or add a specific commit sha
  hooks:
  - id: upgrade-type-hints
    args: [ 'futures=true' ]
```

For more information about available arguments, see the [function definitions](https://github.com/sondrelg/pep585-upgrade/blob/master/src/upgrade_type_hints/update.py#L95).

### Running this once

If you wish to run this once on your codebase, that's not easy to do *without* pre-commit, as it piggybacks on that process quite a bit.

However, installing pre-commit and configuring the hook to run will take you less than a minute. These are the steps:

- Run `pip install pre-commit`
- Run `touch pre-commit-config.yaml`
- Copy the configuration shown above into the file
- Run `pre-commit run --all-files`

### Supporting the project

Please leave a ✭ if this project helped you 👏 and contributions are always welcome!
