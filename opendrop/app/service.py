from injector import Binder, Module, inject, singleton

from opendrop.appfw import QuitService
from opendrop.utility.events import Event


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=AppService, to=AppService, scope=singleton)


class AppService:
    @inject
    def __init__(self, quit_service: QuitService) -> None:
        self._quit_service = quit_service

        self.on_show_start = Event()
        self.on_new_ift_session = Event()
        self.on_new_conan_session = Event()

    def show_start(self) -> None:
        self.on_show_start.fire()

    def new_ift_session(self) -> None:
        self.on_new_ift_session.fire()

    def new_conan_session(self) -> None:
        self.on_new_conan_session.fire()

    def quit(self) -> None:
        self._quit_service.quit()
