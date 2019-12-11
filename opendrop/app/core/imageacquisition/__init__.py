from injector import Module, Binder, singleton

from .acquirers import _AcquirersModule
from .service import ImageAcquisitionService


class ImageAcquisitionModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(_AcquirersModule)
        binder.bind(interface=ImageAcquisitionService, to=ImageAcquisitionService, scope=singleton)
