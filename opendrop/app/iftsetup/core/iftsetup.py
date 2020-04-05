from typing import Mapping

from injector import Module, Binder, inject, singleton

from opendrop.app.commonsetup.core.imageacquirer import ImageAcquirerSetupServiceModule, ImageAcquirerSetupService


class IFTSetupServiceModule(Module):
    def configure(self, binder: Binder):
        binder.install(ImageAcquirerSetupServiceModule)
        binder.bind(interface=IFTSetupService, to=IFTSetupService, scope=singleton)


class IFTSetupService:
    @inject
    def __init__(self, image_acquirer_setup: ImageAcquirerSetupService) -> None:
        self._image_acquirer_setup = image_acquirer_setup

    def set_up(self) -> Mapping:
        try:
            image_acquirer = self._image_acquirer_setup.provide_acquirer()
        except Exception:
            raise

        return dict(
            image_acquirer=image_acquirer
        )
