import typing
from collections import abc
from typing import Iterator, TypeVar, Any, Iterable, Generic

from opendrop.utility.events import Event

T = TypeVar('T')


class BindableSet(abc.MutableSet, Generic[T]):
    def __init__(self, iterable: Iterable[T] = ()) -> None:
        self.on_add = Event()
        self.on_remove = Event()

        self._set = set(iterable)  # type: typing.MutableSet[T]

    def add(self, x: T) -> None:
        if x in self._set: return
        self._set.add(x)
        self.on_add.fire(x)

    def discard(self, x: T) -> None:
        if x in self._set: return
        self._set.remove(x)
        self.on_remove.fire(x)

    def __contains__(self, x: Any) -> bool:
        return x in self._set

    def __len__(self) -> int:
        return len(self._set)

    def __iter__(self) -> Iterator[T]:
        return iter(self._set)

    def __repr__(self) -> str:
        return "BindableSet({})".format(repr(self._set))
