from injector import Module, Binder, singleton
from injector import inject

from opendrop.app.core.imageacquisition import ImageAcquisitionModule
from opendrop.app.core.imageacquisition.service import ImageAcquisitionService


class SessionModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(ImageAcquisitionModule)
        binder.bind(interface=SessionService, to=SessionService, scope=singleton)


class SessionService:
    @inject
    def __init__(self, image_acquisition_service: ImageAcquisitionService) -> None:
        self._image_acquisition_service = image_acquisition_service
