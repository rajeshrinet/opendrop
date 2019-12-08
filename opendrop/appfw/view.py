from typing import Any, Optional

from gi.repository import Gtk


class View:
    def destroy(self) -> None:
        pass


class WidgetView(View):
    _widget = None  # type: Optional[Gtk.Widget]

    def set_widget(self, widget: Any) -> None:
        assert self._widget is None
        self._widget = widget
