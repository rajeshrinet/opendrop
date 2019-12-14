from gi.repository import Gtk
from injector import inject

from opendrop.app.core.imageacquisition.acquirers import FilesystemAcquirerProvider
from opendrop.appfw import WidgetComponent, WidgetView, Presenter
from opendrop.widgets.file_chooser_button import FileChooserButton
from opendrop.widgets.float_entry import FloatEntry


class FilesystemEditorComponent(WidgetComponent):
    pass


@FilesystemEditorComponent.view
class FilesystemEditorView(WidgetView):
    _FILE_INPUT_FILTER = Gtk.FileFilter()
    _FILE_INPUT_FILTER.add_mime_type('image/png')
    _FILE_INPUT_FILTER.add_mime_type('image/jpg')

    def __init__(self) -> None:
        body = Gtk.Grid(row_spacing=5, column_spacing=5)
        self.set_widget(body)

        file_chooser_lbl = Gtk.Label('Image files:', xalign=0)
        body.attach(file_chooser_lbl, 0, 0, 1, 1)

        self._file_chooser_inp = FileChooserButton(
            select_multiple=True
            filter=self._FILE_INPUT_FILTER,
        )
        self._file_chooser_inp.get_style_context().add_class('small-pad')
        body.attach_next_to(self._file_chooser_inp, file_chooser_lbl, Gtk.PositionType.RIGHT, 1, 1)

        frame_interval_lbl = Gtk.Label('Frame interval (s):')
        body.attach(frame_interval_lbl, 0, 1, 1, 1)

        frame_interval_inp_container = Gtk.Grid()
        body.attach_next_to(frame_interval_inp_container, frame_interval_lbl, Gtk.PositionType.RIGHT, 1, 1)

        self._frame_interval_inp = FloatEntry(lower=0, width_chars=6)
        self._frame_interval_inp.get_style_context().add_class('small-pad')
        frame_interval_inp_container.add(self._frame_interval_inp)

        body.foreach(Gtk.Widget.show_all)

@FilesystemEditorComponent.presenter
class FilesystemEditorPresenter(Presenter):
    @inject
    def __init__(self, *, acquirer_provider: FilesystemAcquirerProvider) -> None:
        self._provider = acquirer_provider
