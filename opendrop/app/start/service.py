from injector import Module, Binder, inject

from opendrop.appfw import QuitService


class StartModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=StartService, to=StartService)


class StartService:
    @inject
    def __init__(self, quitter: QuitService) -> None:
        self._quitter = quitter

    def close(self) -> None:
        self._quitter.quit()
