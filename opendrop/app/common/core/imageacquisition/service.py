from typing import Optional

from injector import Module, Binder, singleton

from ..imageacquirer import ImageAcquirer


class ImageAcquisitionServiceModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=ImageAcquisitionService, to=ImageAcquisitionService, scope=singleton)


class ImageAcquisitionService:
    def __init__(self) -> None:
        self.acquirer = None  # type: Optional[ImageAcquirer]
