from gi.repository import Gtk, Gdk
from injector import inject

from opendrop.app.iftsetup import IFTSetupComponent
from opendrop.appfw import WidgetComponent, WidgetView, Presenter, ComponentFactory
from .service import StartServiceModule, StartService


class StartWindow(WidgetComponent):
    modules = [StartServiceModule]


@StartWindow.view
class StartWindowView(WidgetView):
    @inject
    def __init__(self, presenter: 'StartWindowPresenter', cf: ComponentFactory) -> None:
        self._presenter = presenter

        window = Gtk.Window(title='OpenDrop', window_position=Gtk.WindowPosition.CENTER)
        self.set_widget(window)

        body = Gtk.Grid()
        window.add(body)

        setup_stack = Gtk.Stack()
        body.attach(setup_stack, 1, 0, 1, 1)

        sidebar = Gtk.StackSidebar(stack=setup_stack)
        body.attach(sidebar, 0, 0, 1, 1)

        ift_setup = cf.create_widget(IFTSetupComponent)
        setup_stack.add_titled(ift_setup, name='ift', title='Interfacial Tension')

        window.foreach(Gtk.Widget.show_all)

        window.connect('delete-event', self._hdl_window_delete_event)

    def _hdl_window_delete_event(self, window: Gtk.Window, data: Gdk.Event) -> bool:
        self._presenter.hdl_window_request_close()

        # return True to prevent window from closing.
        return True


@StartWindow.presenter
class StartWindowPresenter(Presenter['StartWindowView']):
    @inject
    def __init__(self, service: StartService) -> None:
        self._service = service

    def hdl_window_request_close(self) -> None:
        self._service.close()
