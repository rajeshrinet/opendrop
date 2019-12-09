from typing import Optional

from injector import Binder, Module, inject, singleton

from opendrop.app.ift.component import IFTComponent
from opendrop.app.start.component import StartComponent
from opendrop.appfw import Component, View, Presenter, ComponentFactory
from .service import AppService


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=AppService, to=AppService, scope=singleton)


class AppComponent(Component):
    modules = [AppModule]


@AppComponent.view
class AppView(View):
    @inject
    def __init__(self, cf: ComponentFactory) -> None:
        self._cf = cf

        self._current_component = None

    def clear_current_component(self) -> None:
        if self._current_component is None:
            return

        self._current_component.destroy()

    def set_current_component(self, component: Component) -> None:
        assert self._current_component is None
        self._current_component = component

    def show_start(self) -> None:
        self.clear_current_component()

        start_cmp = self._cf.create(StartComponent)
        start_cmp.widget.show()

        self.set_current_component(start_cmp)

    def new_ift_session(self) -> None:
        print('new_ift_session()')

    def new_conan_session(self) -> None:
        print('new_conan_session()')


@AppComponent.presenter
class AppPresenter(Presenter):
    @inject
    def __init__(self, service: AppService) -> None:
        self._service = service

        self._view = None  # type: Optional[AppView]
        self._before_view_destroy_cleanup_tasks = []

    def after_view_init(self, view: AppView) -> None:
        self._view = view

        connections = [
            self._service.on_show_start.connect(self._hdl_show_start),
            self._service.on_new_ift_session.connect(self._hdl_new_ift_session),
            self._service.on_new_conan_session.connect(self._hdl_new_conan_session),
        ]

        self._before_view_destroy_cleanup_tasks += (
            conn.disconnect
            for conn in connections
        )

        view.show_start()

    def _hdl_show_start(self) -> None:
        self._view.show_start()

    def _hdl_new_ift_session(self) -> None:
        self._view.new_ift_session()

    def _hdl_new_conan_session(self) -> None:
        self._view.new_conan_session()

    def before_view_destroy(self) -> None:
        for f in self._before_view_destroy_cleanup_tasks:
            f()
