from injector import inject, Module, Binder, singleton

from opendrop.app.core.config import Configurator
from opendrop.app.core.imageacquisition_config import ImageAcquisitionConfiguratorModule
from opendrop.app.core.imageacquisition_config.service import ImageAcquisitionConfiguratorService


class SessionConfiguratorModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(ImageAcquisitionConfiguratorModule)

        binder.bind(interface=SessionConfiguratorService, to=SessionConfiguratorService, scope=singleton)


class SessionConfiguratorService(Configurator):
    @inject
    def __init__(self, image_acquisition_config: ImageAcquisitionConfiguratorService) -> None:
        self._image_acquisition_config = image_acquisition_config

    def prepare(self) -> None:
        self._image_acquisition_config.prepare()

    def reset(self) -> None:
        self._image_acquisition_config.reset()

    def install(self) -> None:
        self._image_acquisition_config.install()
