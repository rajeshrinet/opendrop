from injector import Module, Binder, singleton

from .service import ImageAcquisitionConfiguratorService


class ImageAcquisitionConfiguratorModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=ImageAcquisitionConfiguratorService, to=ImageAcquisitionConfiguratorService, scope=singleton)
