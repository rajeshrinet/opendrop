from injector import Module, Binder, inject, singleton

from opendrop.app.common.core.imageacquirer import ImageAcquirer
from opendrop.app.common.core.imageacquisition import ImageAcquisitionServiceModule, ImageAcquisitionService
from opendrop.app.common.core.imagestack import ImageStackServiceModule


class IFTServiceModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(ImageStackServiceModule)
        binder.install(ImageAcquisitionServiceModule)

        binder.bind(interface=IFTService, to=IFTService, scope=singleton)


class IFTService:
    @inject
    def __init__(self, image_acquisition: ImageAcquisitionService) -> None:
        self._image_acquisition = image_acquisition

    def init_session(self, image_acquirer: ImageAcquirer) -> None:
        self._image_acquisition.acquirer = image_acquirer
