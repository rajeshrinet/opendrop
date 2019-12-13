from gi.repository import Gtk, Gdk
from injector import inject

from opendrop.appfw import WidgetComponent, WidgetView, Presenter
from . import StartModule
from .service import StartService


class StartComponent(WidgetComponent):
    modules = [StartModule]


@StartComponent.view
class StartView(WidgetView):
    @inject
    def __init__(self, presenter: 'StartPresenter') -> None:
        self._presenter = presenter

        window = Gtk.Window(title='OpenDrop', window_position=Gtk.WindowPosition.CENTER)
        self.set_widget(window)

        body = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL, margin=10, row_spacing=10)

        window.add(body)

        ift_btn = Gtk.Button('Interfacial Tension')
        body.add(ift_btn)

        conan_btn = Gtk.Button('Contact Angle')
        body.add(conan_btn)

        window.foreach(Gtk.Widget.show_all)

        ift_btn.connect('clicked', lambda *_: presenter.hdl_ift_btn_clicked())
        conan_btn.connect('clicked', lambda *_: presenter.hdl_conan_btn_clicked())
        window.connect('delete-event', self._hdl_window_delete_event)

    def _hdl_window_delete_event(self, window: Gtk.Window, data: Gdk.Event) -> bool:
        self._presenter.hdl_window_request_close()

        # return True to prevent window from closing.
        return True


@StartComponent.presenter
class StartPresenter(Presenter['StartView']):
    @inject
    def __init__(self, service: StartService) -> None:
        self._service = service

    def hdl_ift_btn_clicked(self) -> None:
        self._service.new_ift_session()

    def hdl_conan_btn_clicked(self) -> None:
        self._service.new_conan_session()

    def hdl_window_request_close(self) -> None:
        self._service.close()
