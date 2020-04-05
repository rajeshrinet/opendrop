from injector import Module, Binder, inject, singleton

from opendrop.app.common.core.imageacquirer import ImageAcquirer
from opendrop.app.common.core.imageacquisition import ImageAcquisitionServiceModule, ImageAcquisitionService
from opendrop.app.common.core.imagestack import ImageStackServiceModule
from opendrop.appfw import ActivityControllerService, QuitService


class IFTServiceModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(ImageStackServiceModule)
        binder.install(ImageAcquisitionServiceModule)

        binder.bind(interface=IFTService, to=IFTService, scope=singleton)


class IFTService:
    @inject
    def __init__(
            self,
            activity_controller: ActivityControllerService,
            quitter: QuitService,
            image_acquisition: ImageAcquisitionService,
    ) -> None:
        self._activity_controller = activity_controller
        self._quitter = quitter

        self._image_acquisition = image_acquisition

    def init_session(self, image_acquirer: ImageAcquirer) -> None:
        self._image_acquisition.acquirer = image_acquirer

    def back(self) -> None:
        from opendrop.app.start.window import StartWindow
        self._activity_controller.change_activity(StartWindow)

    def quit(self) -> None:
        self._quitter.quit()
