# PEP585 Upgrade

This is a [pre-commit](https://pre-commit.com/) hook for upgrading type hints 
to the new native types implemented in [PEP 585](https://www.python.org/dev/peps/pep-0585/).

The new types are natively supported as in Python `3.9.0`, but were also backported to version `3.7+`, using the futures import.
A complete list of the new types are shown below.
<details>
<summary>Show all new types</summary>

<br>

| Typing import    	            | Upgraded to  	                                |
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


### Features:
- [x] Performs in-line substitution for new types
- [x] Adds required imports from `collections`, `contextlib`, and `re` types where needed
- [x] Adds `__futures__` imports if the `futures` option is enabled
- [ ] Removes unused typing imports

For more information about available arguments, see the [function definition](https://github.com/sondrelg/pep585-upgrade/blob/master/upgrade_type_hints.py#L90).


### Config

To use this with pre-commit, simply add this to your config file:

```yaml
- repo: https://github.com/sondrelg/pep585-upgrade
  rev: master
  hooks:
  - id: upgrade-type-hints
```

### Running this once

If you wish to run this once on your codebase, that's not possible *without* pre-commit, as it piggybacks on pre-commit quite a bit.

However, installing pre-commit and configuring the hook to run will take you less than a minute. These are the steps:

- Run `pip install pre-commit`
- Run `touch pre-commit-config.yaml`
- Copy the configuration shown above into the file
- Run `pre-commit run --all-files`
