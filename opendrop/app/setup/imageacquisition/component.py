from typing import Type, Optional, Any

from gi.repository import Gtk
from injector import inject

from opendrop.app.core.imageacquisition.acquirers import FilesystemAcquirerProvider, USBCameraAcquirerProvider
from opendrop.app.core.imageacquisition_config.service import ImageAcquisitionConfiguratorService
from opendrop.appfw import WidgetComponent, WidgetView, Presenter, ComponentFactory
from opendrop.utility.bindable.gextension import GObjectPropertyBindable
from ._editors import EditorsModule, EditorResolver, UnknownImageAcquirerProvider


class ImageAcquisitionConfiguratorComponent(WidgetComponent):
    modules = [EditorsModule]


@ImageAcquisitionConfiguratorComponent.view
class ImageAcquisitionConfiguratorView(WidgetView):
    @inject
    def __init__(self, cf: ComponentFactory) -> None:
        self._cf = cf
        self._current_editor = None  # type: Optional[WidgetComponent]

        body = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL, row_spacing=10)
        self.set_widget(body)

        imgsrc_div = Gtk.Grid(orientation=Gtk.Orientation.HORIZONTAL, column_spacing=5)
        body.add(imgsrc_div)

        imgsrc_lbl = Gtk.Label('Image source:', halign=Gtk.Align.START)
        imgsrc_div.add(imgsrc_lbl)

        imgsrc_combobox = Gtk.ComboBoxText()
        imgsrc_div.add(imgsrc_combobox)

        # Combobox option id's must be strings
        imgsrc_combobox.append(id=FilesystemAcquirerProvider.__name__, text='Filesystem')
        imgsrc_combobox.append(id=USBCameraAcquirerProvider.__name__, text='USB Camera')

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

    def change_editor_type(self, editor_cls: Optional[Type[WidgetComponent]], acquirer_provider: Any) -> None:
        if editor_cls is not None and isinstance(self._current_editor, editor_cls):
            return

        self._clear_editor()

        if editor_cls is None:
            return

        editor = self._cf.create(editor_cls, factory=acquirer_provider)
        self._current_editor = editor

        self._editor_container.add(editor.widget)
        editor.widget.show()


@ImageAcquisitionConfiguratorComponent.presenter
class ImageAcquisitionConfiguratorPresenter(Presenter[ImageAcquisitionConfiguratorView]):
    @inject
    def __init__(self, service: ImageAcquisitionConfiguratorService, resolver: EditorResolver) -> None:
        self._service = service
        self._resolver = resolver

        self._view = None  # type: Optional[ImageAcquisitionConfiguratorView]
        self._before_view_destroy_cleanup_tasks = []

    def after_view_init(self, view: ImageAcquisitionConfiguratorView) -> None:
        self._view = view

        connections = [
            self._view.imgsrc_combobox_selection.on_changed.connect(self._hdl_imgsrc_combobox_selection_changed),
            self._service.acquirer_provider.on_changed.connect(self._hdl_acquirer_provider_changed),
        ]
        self._before_view_destroy_cleanup_tasks += (
            conn.disconnect for conn in connections
        )

        self._hdl_acquirer_provider_changed()

    def _hdl_acquirer_provider_changed(self) -> None:
        acquirer_provider = self._service.acquirer_provider.get()

        try:
            editor_cls = self._resolver.resolve(acquirer_provider)
        except UnknownImageAcquirerProvider:
            editor_cls = None

        self._view.change_editor_type(editor_cls, acquirer_provider=acquirer_provider)

        provider_cls = type(acquirer_provider)
        self._view.imgsrc_combobox_selection.set(provider_cls.__name__)

    def _hdl_imgsrc_combobox_selection_changed(self) -> None:
        selection = self._view.imgsrc_combobox_selection.get()
        if selection is None:
            return

        new_provider_cls = eval(selection)

        current_provider = self._service.acquirer_provider.get()
        current_provider_cls = type(current_provider)

        if new_provider_cls is current_provider_cls:
            return

        self._service.change_provider_type(new_provider_cls)

    def before_view_destroy(self) -> None:
        for f in self._before_view_destroy_cleanup_tasks:
            f()
