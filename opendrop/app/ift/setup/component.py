from gi.repository import Gtk, Gdk
from injector import inject, Module, Binder, singleton

from opendrop.app.ift.setup.service import SetupService
from opendrop.appfw import WidgetComponent, WidgetView, Presenter


class SetupModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=SetupService, to=SetupService, scope=singleton)


class SetupComponent(WidgetComponent):
    modules = [SetupModule]


@SetupComponent.view
class SetupView(WidgetView):
    @inject
    def __init__(self, presenter: 'SetupPresenter') -> None:
        self._presenter = presenter

        window = Gtk.Window(title='Interfacial Tension Setup',  window_position=Gtk.WindowPosition.CENTER)
        self.set_widget(window)

        body = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        window.add(body)

        body.add(Gtk.Label('Setup', hexpand=True, vexpand=True))
        body.add(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        action_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5, margin=5)
        body.add(action_area)

        continue_btn = Gtk.Button('Continue')
        continue_btn.get_style_context().add_class('suggested-action')
        action_area.pack_end(continue_btn, expand=False, fill=False, padding=0)

        cancel_btn = Gtk.Button('Cancel')
        action_area.pack_end(cancel_btn, expand=False, fill=False, padding=0)

        continue_btn.connect('clicked', lambda *_: self._presenter.hdl_continue_btn_clicked())
        cancel_btn.connect('clicked', lambda *_: self._presenter.hdl_cancel_btn_clicked())
        window.connect('delete-event', self._hdl_window_delete_event)

        window.foreach(Gtk.Widget.show_all)

    def _hdl_window_delete_event(self, window: Gtk.Window, data: Gdk.Event) -> bool:
        self._presenter.hdl_window_close()

        # return True to prevent window from closing.
        return True


@SetupComponent.presenter
class SetupPresenter(Presenter['SetupView']):
    @inject
    def __init__(self, service: SetupService) -> None:
        self._service = service

    def hdl_continue_btn_clicked(self) -> None:
        self._service.submit()

    def hdl_cancel_btn_clicked(self) -> None:
        self._service.cancel()

    def hdl_window_close(self) -> None:
        self._service.close()
