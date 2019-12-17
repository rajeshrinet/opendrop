from injector import Module, Binder, inject, singleton

from opendrop.appfw import ActivityControllerService, QuitService
from .core import SessionModule


class IFTModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(SessionModule)
        binder.bind(interface=IFTService, to=IFTService, scope=singleton)


class IFTService:
    @inject
    def __init__(self, activity_controller: ActivityControllerService, quitter: QuitService) -> None:
        self._activity_controller = activity_controller
        self._quitter = quitter

    def back(self) -> None:
        from opendrop.app.start.component import StartComponent
        self._activity_controller.start_activity(StartComponent)

    def quit(self) -> None:
        self._quitter.quit()
