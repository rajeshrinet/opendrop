from typing import Optional, Tuple

import cairo
from gi.repository import Gtk, GObject, Gdk

from .abc import Composition


class CompositionArea(Gtk.DrawingArea):
    _composition = None  # type: Optional[Composition]

    _hdl_composition_invalidate_event_id = None  # type: Optional[int]
    _mapped = False

    def do_draw(self, cr: cairo.Context) -> None:
        if self._composition is None:
            return

        self._composition.draw(cr)

    @GObject.Property
    def composition(self) -> Composition:
        return self._composition

    @composition.setter
    def composition(self, value: Composition) -> None:
        self._disconnect_composition()
        self._composition = value
        self._connect_composition()
        self.queue_draw()

    def _connect_composition(self) -> None:
        self._hdl_composition_invalidate_event_id = self._composition.connect(
            'invalidate-event', self._hdl_composition_invalidate_event
        )
        self._update_composition_mapped()

    def _disconnect_composition(self) -> None:
        if self._composition is None:
            return

        self._composition.unmap()
        self._composition.disconnect(self._hdl_composition_invalidate_event_id)

    def _update_composition_mapped(self) -> None:
        if self._composition is None:
            return

        if self._mapped:
            self._composition.map()
        else:
            self._composition.unmap()

    def _update_composition_size(self, size: Tuple[int, int]) -> None:
        if self._composition is None:
            return

        self._composition.size_allocate(size)

    def _hdl_composition_invalidate_event(self, region: cairo.Region) -> None:
        self.queue_draw_region(region)

    def do_map(self) -> None:
        Gtk.DrawingArea.do_map(self)
        self._mapped = True
        self._update_composition_mapped()

    def do_unmap(self) -> None:
        Gtk.DrawingArea.do_unmap(self)
        self._mapped = False
        self._update_composition_mapped()

    def do_size_allocate(self, allocation: Gdk.Rectangle) -> None:
        Gtk.DrawingArea.do_size_allocate(self, allocation)
        self._update_composition_size((allocation.width, allocation.height))
