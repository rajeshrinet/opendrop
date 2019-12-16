from injector import Module, Binder, singleton

from opendrop.app.core.imageacquirer import ImageAcquirer


class ImageAcquisitionModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=ImageAcquisitionService, to=ImageAcquisitionService, scope=singleton)


class ImageAcquisitionService:
    def __init__(self) -> None:
        self.is_ready = False
        self.acquirer = None

    def use_acquirer(self, acquirer: ImageAcquirer) -> None:
        self.acquirer = acquirer
        self.is_ready = True
