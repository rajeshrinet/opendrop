from typing import Any

from injector import Module, Binder, singleton

from .acquirers import _AcquirersModule


class ImageAcquisitionModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(_AcquirersModule)
        binder.bind(interface=ImageAcquisitionService, to=ImageAcquisitionService, scope=singleton)


class ImageAcquisitionService:
    def __init__(self) -> None:
        self.is_ready = False
        self.acquirer = None

    def use_acquirer(self, acquirer: Any) -> None:
        self.acquirer = acquirer
        self.is_ready = True
