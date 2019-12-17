from injector import Module, Binder, inject

from opendrop.appfw import ActivityControllerService, QuitService


class StartModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=StartService, to=StartService)


class StartService:
    @inject
    def __init__(self, activity_controller: ActivityControllerService, quitter: QuitService) -> None:
        self._activity_controller = activity_controller
        self._quitter = quitter

    def new_ift_session(self) -> None:
        from opendrop.app.ift.component import IFTComponent
        self._activity_controller.start_activity(IFTComponent)

    def new_conan_session(self) -> None:
        print('new_conan_session()')

    def close(self) -> None:
        self._quitter.quit()
