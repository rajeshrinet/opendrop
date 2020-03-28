from injector import Module, Binder, inject, singleton

from opendrop.app.commonsetup.core.imageacquisition import ImageAcquisitionSetupModule, ImageAcquisitionSetupService
from opendrop.app.ift.component import IFTComponent
from opendrop.appfw import ActivityControllerService


class IFTSetupModule(Module):
    def configure(self, binder: Binder):
        binder.install(ImageAcquisitionSetupModule)
        binder.bind(interface=IFTSetupService, to=IFTSetupService, scope=singleton)


class IFTSetupService:
    @inject
    def __init__(self, image_acquisition_setup: ImageAcquisitionSetupService, activity_controller: ActivityControllerService) -> None:
        self._activity_controller = activity_controller
        self._image_acquisition_setup = image_acquisition_setup

    def set_up(self) -> None:
        try:
            image_acquirer = self._image_acquisition_setup.get_acquirer()
        except Exception:
            raise

        self._activity_controller.start_activity(IFTComponent, image_acquirer=image_acquirer)
