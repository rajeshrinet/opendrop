from gi.repository import Gtk, Gdk
from injector import inject

from opendrop.app.ift.core.session import SessionService
from opendrop.appfw import Presenter, ComponentFactory, WidgetView, WidgetComponent
from . import _IFTModule
from .service import IFTService


class IFTComponent(WidgetComponent):
    modules = [_IFTModule]


@IFTComponent.view
class IFTView(WidgetView):
    @inject
    def __init__(self, presenter: 'IFTPresenter', cf: ComponentFactory) -> None:
        self._presenter = presenter
        self._cf = cf

        window = Gtk.Window(title='Interfacial Tension', window_position=Gtk.WindowPosition.CENTER)
        self.set_widget(window)

        window.connect('delete-event', self._hdl_window_delete_event)
        window.show()

    def _hdl_window_delete_event(self, window: Gtk.Window, data: Gdk.Event) -> bool:
        self._presenter.hdl_window_close()

        # return True to prevent window from closing.
        return True


@IFTComponent.presenter
class IFTPresenter(Presenter[IFTView]):
    @inject
    def __init__(self, service: IFTService, *, session: SessionService) -> None:
        self._service = service
        self._service.set_session(session)

    def hdl_window_close(self) -> None:
        self._service.back()
