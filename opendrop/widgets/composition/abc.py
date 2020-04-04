from typing import Tuple, Optional

import cairo
from gi.repository import GObject


class Composition(GObject.Object):
    _size = (0, 0)

    def draw(self, cr: cairo.Context) -> None:
        pass

    def map(self) -> None:
        pass

    def unmap(self) -> None:
        pass

    def _do_size_allocate(self, size: Tuple[int, int]) -> None:
        pass

    @GObject.Property
    def size(self) -> Tuple[int, int]:
        return self._size

    def size_allocate(self, value: Tuple[int, int]) -> None:
        self._do_size_allocate(value)
        self._size = value

    def invalidate(self, region: Optional[cairo.Region] = None) -> None:
        if region is None:
            region = cairo.Region(cairo.RectangleInt(0, 0, self._size[0], self._size[1]))

        self.emit('invalidate-event', region)

    @GObject.Signal(arg_types=(object,))
    def invalidate_event(self, region: cairo.Region) -> None:
        """Let the parent know that `region` has been invalidated"""
