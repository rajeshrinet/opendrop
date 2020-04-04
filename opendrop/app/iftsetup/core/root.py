from injector import Module, Binder, inject, singleton

from opendrop.app.commonsetup.core.imageacquirer import ImageAcquirerSetupServiceModule, ImageAcquirerSetupService
from opendrop.app.ift.window import IFTWindow
from opendrop.appfw import ActivityControllerService


class IFTSetupRootServiceModule(Module):
    def configure(self, binder: Binder):
        binder.install(ImageAcquirerSetupServiceModule)
        binder.bind(interface=IFTSetupRootService, to=IFTSetupRootService, scope=singleton)


class IFTSetupRootService:
    @inject
    def __init__(self, image_acquirer_setup: ImageAcquirerSetupService, activity_controller: ActivityControllerService)\
            -> None:
        self._activity_controller = activity_controller
        self._image_acquirer_setup = image_acquirer_setup

    def set_up(self) -> None:
        try:
            image_acquirer = self._image_acquirer_setup.provide_acquirer()
        except Exception:
            raise

        self._activity_controller.start_activity(IFTWindow, image_acquirer=image_acquirer)
