from injector import Module, Binder, inject, singleton

from opendrop.app.core.imageacquisition_config import ImageAcquisitionConfiguratorModule
from opendrop.app.core.imageacquisition_config.service import ImageAcquisitionConfiguratorService


class SetupModule(Module):
    def configure(self, binder: Binder):
        binder.install(ImageAcquisitionConfiguratorModule)
        binder.bind(interface=SetupService, to=SetupService, scope=singleton)


class SetupService:
    @inject
    def __init__(self, image_acquisition_config: ImageAcquisitionConfiguratorService) -> None:
        self._image_acquisition_config = image_acquisition_config
