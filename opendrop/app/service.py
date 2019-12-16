from typing import Type

from injector import Binder, Module, inject, singleton

from opendrop.appfw import QuitService, Component
from opendrop.utility.events import Event


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=AppService, to=AppService, scope=singleton)


class AppService:
    @inject
    def __init__(self, quitter: QuitService) -> None:
        self._quitter = quitter

        self.on_start_activity = Event()

    def start_activity(self, component_cls: Type[Component], **kwargs) -> None:
        self.on_start_activity.fire(component_cls, kwargs)

    def quit(self) -> None:
        self._quitter.quit()
