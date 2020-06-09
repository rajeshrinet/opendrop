from gi.repository import Gtk, Gdk
from injector import inject

from opendrop.appfw import WidgetComponent, WidgetView, Presenter, ComponentFactory
from opendrop.appfw import QuitService


class StartWindow(WidgetComponent):
    modules = []


@StartWindow.view
class StartWindowView(WidgetView):
    @inject
    def __init__(self, presenter: 'StartWindowPresenter', cf: ComponentFactory) -> None:
        self._presenter = presenter

        window = Gtk.Window(title='OpenDrop', window_position=Gtk.WindowPosition.CENTER)
        self.set_widget(window)

        body = Gtk.Grid()
        window.add(body)

        window.foreach(Gtk.Widget.show_all)

        window.connect('delete-event', self._hdl_window_delete_event)

    def _hdl_window_delete_event(self, window: Gtk.Window, data: Gdk.Event) -> bool:
        self._presenter.hdl_window_request_close()

        # return True to prevent window from closing.
        return True


@StartWindow.presenter
class StartWindowPresenter(Presenter['StartWindowView']):
    @inject
    def __init__(self, quit_service: QuitService) -> None:
        self._quit_service = quit_service

    def hdl_window_request_close(self) -> None:
        self._quit_service.quit()
