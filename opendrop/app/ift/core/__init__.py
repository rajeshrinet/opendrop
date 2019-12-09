from injector import Module, Binder, singleton

from .service import IFTSessionService


class IFTSessionModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=IFTSessionService, to=IFTSessionService, scope=singleton)
