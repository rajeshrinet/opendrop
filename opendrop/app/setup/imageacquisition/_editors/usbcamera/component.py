from gi.repository import Gtk
from injector import inject

from opendrop.app.core.imageacquirer.usbcamera import USBCameraAcquirerProvider
from opendrop.appfw import WidgetComponent, WidgetView, Presenter
from opendrop.widgets.float_entry import FloatEntry


class USBCameraEditorComponent(WidgetComponent):
    pass


@USBCameraEditorComponent.view
class USBCameraEditorView(WidgetView):
    def __init__(self) -> None:
        body = Gtk.Grid(row_spacing=5, column_spacing=5)
        self.set_widget(body)

        camera_index_lbl = Gtk.Label('Camera index:')
        body.attach(camera_index_lbl, 0, 0, 1, 1)

        camera_index_entry = FloatEntry(lower=0, width_chars=6)
        body.attach(camera_index_entry, 1, 0, 1, 1)

        body.foreach(Gtk.Widget.show_all)


@USBCameraEditorComponent.presenter
class USBCameraPresenter(Presenter):
    @inject
    def __init__(self, *, acquirer_provider: USBCameraAcquirerProvider) -> None:
        self._provider = acquirer_provider
