from gi.repository import Gtk, Gdk
from injector import inject

from opendrop.appfw import Presenter, ComponentFactory, WidgetView, WidgetComponent, ActivityControllerService
from .component import IFTComponent
from .core.ift import IFTServiceModule, IFTService


class IFTWindow(WidgetComponent):
    modules = [IFTServiceModule]


@IFTWindow.view
class IFTWindowView(WidgetView):
    @inject
    def __init__(self, presenter: 'IFTWindowPresenter', cf: ComponentFactory) -> None:
        self._presenter = presenter
        self._cf = cf

        window = Gtk.Window(title='Interfacial Tension', window_position=Gtk.WindowPosition.CENTER)
        self.set_widget(window)

        body = cf.create_widget(IFTComponent, **presenter.ift_recipe)
        body.show()

        window.add(body)

        window.connect('delete-event', self._hdl_window_delete_event)
        window.show()

    def _hdl_window_delete_event(self, window: Gtk.Window, data: Gdk.Event) -> bool:
        self._presenter.hdl_window_close()

        # return True to prevent window from closing.
        return True


@IFTWindow.presenter
class IFTWindowPresenter(Presenter[IFTWindowView]):
    @inject
    def __init__(
            self,
            activity_controller: ActivityControllerService,
            service: IFTService,
            **ift_recipe
    ) -> None:
        self._activity_controller = activity_controller

        self._service = service
        self.ift_recipe = ift_recipe

    def hdl_window_close(self) -> None:
        from opendrop.app.start import StartWindow
        self._activity_controller.change_activity(StartWindow)
