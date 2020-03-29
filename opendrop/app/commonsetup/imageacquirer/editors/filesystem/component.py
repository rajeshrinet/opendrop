import math
from typing import Optional, MutableSequence, Callable

from gi.repository import Gtk
from injector import inject

from opendrop.app.common.core.imageacquirer.filesystem import FilesystemAcquirerProvider
from opendrop.appfw import WidgetComponent, WidgetView, Presenter
from opendrop.utility.bindable.gextension import GObjectPropertyBindable
from opendrop.widgets.file_chooser_button import FileChooserButton
from opendrop.widgets.float_entry import FloatEntry


class FilesystemEditorComponent(WidgetComponent):
    pass


@FilesystemEditorComponent.view
class FilesystemEditorView(WidgetView):
    _FILE_CHOOSER_FILTER = Gtk.FileFilter()
    _FILE_CHOOSER_FILTER.add_mime_type('image/png')
    _FILE_CHOOSER_FILTER.add_mime_type('image/jpg')

    def __init__(self) -> None:
        body = Gtk.Grid(row_spacing=5, column_spacing=5)
        self.set_widget(body)

        file_chooser_lbl = Gtk.Label('Image files:', xalign=0)
        body.attach(file_chooser_lbl, 0, 0, 1, 1)

        file_chooser_btn = FileChooserButton(
            filter=self._FILE_CHOOSER_FILTER,
            select_multiple=True,
        )
        file_chooser_btn.get_style_context().add_class('small-pad')
        body.attach_next_to(file_chooser_btn, file_chooser_lbl, Gtk.PositionType.RIGHT, 1, 1)

        frame_interval_lbl = Gtk.Label('Frame interval (s):')
        body.attach(frame_interval_lbl, 0, 1, 1, 1)

        frame_interval_inp_container = Gtk.Grid()
        body.attach_next_to(frame_interval_inp_container, frame_interval_lbl, Gtk.PositionType.RIGHT, 1, 1)

        frame_interval_entry = FloatEntry(default=math.nan, lower=0, width_chars=6)
        frame_interval_entry.get_style_context().add_class('small-pad')
        frame_interval_inp_container.add(frame_interval_entry)

        self.image_paths = GObjectPropertyBindable(
            g_obj=file_chooser_btn,
            prop_name='file-paths',
        )

        self.frame_interval = GObjectPropertyBindable(
            g_obj=frame_interval_entry,
            prop_name='value',
        )

        body.foreach(Gtk.Widget.show_all)


@FilesystemEditorComponent.presenter
class FilesystemEditorPresenter(Presenter[FilesystemEditorView]):
    @inject
    def __init__(self, *, acquirer_provider: FilesystemAcquirerProvider) -> None:
        self._provider = acquirer_provider

        self._view = None  # type: Optional[FilesystemEditorView]
        self._before_view_destroy_cleanup_tasks = []  # type: MutableSequence[Callable]

    def after_view_init(self, view: FilesystemEditorView) -> None:
        self._view = view

        bindings = [
            self._provider.frame_interval.bind(view.frame_interval),
            self._provider.image_paths.bind(view.image_paths),
        ]

        self._before_view_destroy_cleanup_tasks += (
            binding.unbind for binding in bindings
        )

    def before_view_destroy(self) -> None:
        for f in self._before_view_destroy_cleanup_tasks:
            f()
