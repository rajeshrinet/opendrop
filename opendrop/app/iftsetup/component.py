from typing import Optional

from gi.repository import Gtk, Gdk
from injector import inject

from opendrop.app.common.core.imageacquirer.filesystem import EmptyPathsError
from opendrop.app.commonsetup.imageacquirer import ImageAcquirerSetupEditor
from opendrop.appfw import WidgetComponent, WidgetView, Presenter, ComponentFactory, WindowContext
from opendrop.widgets.error_dialog import ErrorDialog
from .core.root import IFTSetupRootServiceModule, IFTSetupRootService


class IFTSetupComponent(WidgetComponent):
    modules = [IFTSetupRootServiceModule]


@IFTSetupComponent.view
class IFTSetupView(WidgetView):
    @inject
    def __init__(self, presenter: 'IFTSetupPresenter', window_ctx: WindowContext, cf: ComponentFactory) -> None:
        self._presenter = presenter
        self._window_ctx = window_ctx

        body = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        self.set_widget(body)

        content_area = Gtk.Grid(hexpand=True, vexpand=True, margin=5)
        body.add(content_area)

        # body.add(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        action_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, hexpand=True, spacing=5, margin=5)
        body.add(action_area)

        image_acquisition_frame = Gtk.Frame(label='Image acquisition', hexpand=True, vexpand=True)
        content_area.add(image_acquisition_frame)

        image_acquirer_setup = cf.create_widget(ImageAcquirerSetupEditor)
        image_acquirer_setup.props.margin = 10
        image_acquisition_frame.add(image_acquirer_setup)

        continue_btn = Gtk.Button('Continue')
        continue_btn.get_style_context().add_class('suggested-action')
        action_area.pack_end(continue_btn, expand=False, fill=False, padding=0)
        #
        # cancel_btn = Gtk.Button('Cancel')
        # action_area.pack_end(cancel_btn, expand=False, fill=False, padding=0)

        continue_btn.connect('clicked', lambda *_: self._presenter.hdl_continue_btn_clicked())
        # cancel_btn.connect('clicked', lambda *_: self._presenter.hdl_cancel_btn_clicked())

        body.foreach(Gtk.Widget.show_all)

    def _hdl_window_delete_event(self, window: Gtk.Window, data: Gdk.Event) -> bool:
        self._presenter.hdl_window_close()

        # return True to prevent window from closing.
        return True

    _is_showing_error = False

    def show_error(self, error: Exception) -> None:
        error_text = ''
        if isinstance(error, EmptyPathsError):
            error_text = 'Image files cannot be empty.'
        else:
            raise error

        if self._is_showing_error:
            return

        self._is_showing_error = True

        error_dialog = ErrorDialog(
            parent=self._window_ctx.window,
            title='Error',
            text=error_text,
        )

        error_dialog.connect('response', self._hdl_error_dialog_response)
        error_dialog.connect('destroy', self._hdl_error_dialog_destroy)

        error_dialog.show()

    def _hdl_error_dialog_response(self, dialog: Gtk.Widget, response: Gtk.ResponseType) -> None:
        dialog.destroy()

    def _hdl_error_dialog_destroy(self, dialog: Gtk.Widget) -> None:
        self._is_showing_error = False


@IFTSetupComponent.presenter
class IFTSetupPresenter(Presenter[IFTSetupView]):
    @inject
    def __init__(self, service: IFTSetupRootService) -> None:
        self._service = service

        self._view = None  # type: Optional[IFTSetupView]

    def after_view_init(self, view: IFTSetupView) -> None:
        self._view = view

    def hdl_continue_btn_clicked(self) -> None:
        try:
            self._service.set_up()
        except Exception as e:
            self._view.show_error(e)
