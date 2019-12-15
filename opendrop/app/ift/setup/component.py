from typing import Optional, Callable, Any

from gi.repository import Gtk, Gdk
from injector import inject

from opendrop.app.ift.core import SetupModule
from opendrop.app.ift.core.setup_service import SetupService
from opendrop.app.setup.imageacquisition.component import ImageAcquisitionConfiguratorComponent
from opendrop.appfw import WidgetComponent, WidgetView, Presenter, ComponentFactory
from opendrop.widgets.error_dialog import ErrorDialog


class SetupComponent(WidgetComponent):
    modules = [SetupModule]


@SetupComponent.view
class SetupView(WidgetView):
    @inject
    def __init__(self, presenter: 'SetupPresenter', cf: ComponentFactory) -> None:
        self._presenter = presenter

        window = Gtk.Window(title='Interfacial Tension Setup',  window_position=Gtk.WindowPosition.CENTER)
        self.set_widget(window)

        body = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        window.add(body)

        content_area = Gtk.Grid(hexpand=True, vexpand=True, margin=5)
        body.add(content_area)

        body.add(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        action_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, hexpand=True, spacing=5, margin=5)
        body.add(action_area)

        image_acquisition_frame = Gtk.Frame(label='Image acquisition', hexpand=True, vexpand=True)
        content_area.add(image_acquisition_frame)

        image_acquisition_configurator_cmp = cf.create(ImageAcquisitionConfiguratorComponent)
        image_acquisition_configurator_cmp.widget.props.margin = 10
        image_acquisition_frame.add(image_acquisition_configurator_cmp.widget)

        continue_btn = Gtk.Button('Continue')
        continue_btn.get_style_context().add_class('suggested-action')
        action_area.pack_end(continue_btn, expand=False, fill=False, padding=0)

        cancel_btn = Gtk.Button('Cancel')
        action_area.pack_end(cancel_btn, expand=False, fill=False, padding=0)

        continue_btn.connect('clicked', lambda *_: self._presenter.hdl_continue_btn_clicked())
        cancel_btn.connect('clicked', lambda *_: self._presenter.hdl_cancel_btn_clicked())
        window.connect('delete-event', self._hdl_window_delete_event)

        window.foreach(Gtk.Widget.show_all)

        self._window = window

    def _hdl_window_delete_event(self, window: Gtk.Window, data: Gdk.Event) -> bool:
        self._presenter.hdl_window_close()

        # return True to prevent window from closing.
        return True

    def show_error(self, error: Any) -> None:
        error_dialog = ErrorDialog(
            parent=self._window,
            title='Error',
            text=str(error),
        )

        error_dialog.connect('response', lambda *_: error_dialog.destroy())

        error_dialog.show()


@SetupComponent.presenter
class SetupPresenter(Presenter['SetupView']):
    @inject
    def __init__(self, service: SetupService, *, on_success: Optional[Callable] = None, on_cancel: Optional[Callable] = None, on_close: Optional[Callable] = None) -> None:
        self._service = service

        self._on_success = on_success or (lambda: None)
        self._on_cancel = on_cancel or (lambda: None)
        self._on_close = on_close or (lambda: None)

        self._view = None  # type: Optional[SetupView]

    def after_view_init(self, view: SetupView) -> None:
        self._view = view

    def hdl_continue_btn_clicked(self) -> None:
        error = self._service.set_up()
        if error:
            self._view.show_error(error)
            return

        self._on_success()

    def hdl_cancel_btn_clicked(self) -> None:
        self._on_cancel()

    def hdl_window_close(self) -> None:
        self._on_close()
