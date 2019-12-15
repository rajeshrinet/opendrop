import gi
from gi.repository import Gtk

gi.require_version('Gtk', '3.0')

from opendrop.appfw import WidgetComponent, WidgetView, Presenter


class MyWidgetComponent(WidgetComponent):
    pass


@MyWidgetComponent.view
class MyWidgetView(WidgetView):
    def __init__(self) -> None:
        widget = Gtk.Grid()
        self.set_widget(widget)


@MyWidgetComponent.presenter
class MyWidgetPresenter(Presenter):
    pass


def test_WidgetComponent_destroys_after_widget_is_destroyed():
    component = MyWidgetComponent()
    component.widget.destroy()
    assert component._is_destroyed
