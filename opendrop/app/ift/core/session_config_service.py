from typing import MutableMapping

from injector import inject, Module, Binder, singleton

from opendrop.app.core.config import Configurator, Installer, PreparationError
from opendrop.app.core.imageacquisition_config import ImageAcquisitionConfiguratorModule
from opendrop.app.core.imageacquisition_config.service import (
    ImageAcquisitionConfiguratorService,
    ImageAcquisitionInstaller,
)
from .session_service import SessionService


class SessionConfiguratorModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(ImageAcquisitionConfiguratorModule)

        binder.bind(interface=SessionConfiguratorService, to=SessionConfiguratorService, scope=singleton)


class SessionConfiguratorService(Configurator[SessionService]):
    @inject
    def __init__(self, image_acquisition_config: ImageAcquisitionConfiguratorService) -> None:
        self._image_acquisition_config = image_acquisition_config

    def prepare(self) -> 'SessionInstaller':
        installers = {}  # type: MutableMapping[str, Installer]

        try:
            installers['image_acquisition_installer'] = self._image_acquisition_config.prepare()
        except PreparationError:
            for installer in installers.values():
                installer.destroy()

            raise

        return SessionInstaller(**installers)


class SessionInstaller(Installer[SessionService]):
    def __init__(self, image_acquisition_installer: ImageAcquisitionInstaller):
        self._image_acquisition_installer = image_acquisition_installer

    def install(self, target: SessionService) -> None:
        self._image_acquisition_installer.install(target.image_acquisition_service)

    def destroy(self) -> None:
        self._image_acquisition_installer.destroy()
