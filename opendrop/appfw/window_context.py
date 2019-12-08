from typing import Optional

from gi.repository import Gtk
from injector import inject, Module, Binder

from .component import WidgetComponent, _Component


class _WindowContextModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=WindowContext, to=WindowContext)


class WindowContext:
    @inject
    def __init__(self, scope: _Component) -> None:
        self._scope = scope

    @property
    def window(self) -> Optional[Gtk.Window]:
        outer_scope = self._scope._parent

        while outer_scope is not None:
            if not isinstance(outer_scope, WidgetComponent):
                outer_scope = outer_scope._parent
                continue

            if not isinstance(outer_scope.widget, Gtk.Window):
                outer_scope = outer_scope._parent
                continue

            return outer_scope.widget

        return None
