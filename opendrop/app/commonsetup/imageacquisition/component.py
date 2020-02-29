from typing import Type, Optional

from gi.repository import Gtk
from injector import inject

from opendrop.app.common.core.imageacquirer import FilesystemAcquirer, USBCameraAcquirer, ImageAcquirerProvider
from opendrop.app.common.core.setup.imageacquisition import ImageAcquisitionSetupService
from opendrop.appfw import WidgetComponent, WidgetView, Presenter, ComponentFactory
from opendrop.utility.bindable.gextension import GObjectPropertyBindable
from .editors import EditorsModule, EditorResolver, UnknownImageAcquirerProvider


class ImageAcquisitionConfiguratorComponent(WidgetComponent):
    modules = [EditorsModule]


@ImageAcquisitionConfiguratorComponent.view
class ImageAcquisitionConfiguratorView(WidgetView):
    @inject
    def __init__(self, cf: ComponentFactory) -> None:
        self._cf = cf
        self._current_editor = None  # type: Optional[Gtk.Widget]

        body = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL, row_spacing=10)
        self.set_widget(body)

        imgsrc_div = Gtk.Grid(orientation=Gtk.Orientation.HORIZONTAL, column_spacing=5)
        body.add(imgsrc_div)

        imgsrc_lbl = Gtk.Label('Image source:', halign=Gtk.Align.START)
        imgsrc_div.add(imgsrc_lbl)

        imgsrc_combobox = Gtk.ComboBoxText()
        imgsrc_div.add(imgsrc_combobox)

        # Combobox option id's must be strings
        imgsrc_combobox.append(id=FilesystemAcquirer.__name__, text='Filesystem')
        imgsrc_combobox.append(id=USBCameraAcquirer.__name__, text='USB Camera')

        editor_container = Gtk.Grid()
        body.add(editor_container)

        self._editor_container = editor_container

        self.imgsrc_combobox_selection = GObjectPropertyBindable(
            g_obj=imgsrc_combobox,
            prop_name='active-id',
        )

        body.foreach(Gtk.Widget.show_all)

    def _clear_editor(self) -> None:
        if self._current_editor is None:
            return

        self._current_editor.destroy()
        self._current_editor = None

    def change_editor_type(self, editor_cls: Optional[Type[WidgetComponent]], acquirer_provider: ImageAcquirerProvider)\
            -> None:
        self._clear_editor()

        if editor_cls is None:
            return

        editor = self._cf.create_widget(editor_cls, acquirer_provider=acquirer_provider)
        self._current_editor = editor

        self._editor_container.add(editor)
        editor.show()


@ImageAcquisitionConfiguratorComponent.presenter
class ImageAcquisitionConfiguratorPresenter(Presenter[ImageAcquisitionConfiguratorView]):
    @inject
    def __init__(self, service: ImageAcquisitionSetupService, resolver: EditorResolver) -> None:
        self._service = service
        self._resolver = resolver

        self._view = None  # type: Optional[ImageAcquisitionConfiguratorView]
        self._before_view_destroy_cleanup_tasks = []

    def after_view_init(self, view: ImageAcquisitionConfiguratorView) -> None:
        self._view = view

        connections = [
            self._view.imgsrc_combobox_selection.on_changed.connect(self._hdl_imgsrc_combobox_selection_changed),
            self._service.provider.on_changed.connect(self._hdl_provider_changed),
        ]
        self._before_view_destroy_cleanup_tasks += (
            conn.disconnect for conn in connections
        )

        self._hdl_provider_changed()

    def _hdl_provider_changed(self) -> None:
        acquirer_provider = self._service.provider.get()

        try:
            editor_cls = self._resolver.resolve(acquirer_provider)
        except UnknownImageAcquirerProvider:
            editor_cls = None

        self._view.change_editor_type(editor_cls, acquirer_provider=acquirer_provider)

        acquirer_cls = acquirer_provider.provides
        self._view.imgsrc_combobox_selection.set(acquirer_cls.__name__)

    def _hdl_imgsrc_combobox_selection_changed(self) -> None:
        selection = self._view.imgsrc_combobox_selection.get()
        if selection is None:
            return

        new_acquirer_cls = eval(selection)

        current_provider = self._service.provider.get()
        current_acquirer_cls = current_provider.provides

        if new_acquirer_cls is current_acquirer_cls:
            return

        self._service.change_acquirer_type(new_acquirer_cls)

    def before_view_destroy(self) -> None:
        for f in self._before_view_destroy_cleanup_tasks:
            f()
