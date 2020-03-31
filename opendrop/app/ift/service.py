from typing import Optional

from injector import Module, Binder, inject, singleton, provider

from opendrop.app.common.core.imageacquirer import ImageAcquirer
from opendrop.app.common.core.imagestack import ImageStackModule
from opendrop.appfw import ActivityControllerService, QuitService


class IFTModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(ImageStackModule)

        binder.bind(interface=IFTService, to=IFTService, scope=singleton)

    @provider
    def image_acquirer(self, root: 'IFTService') -> ImageAcquirer:
        return root._image_acquirer


class IFTService:
    @inject
    def __init__(self, activity_controller: ActivityControllerService, quitter: QuitService) -> None:
        self._activity_controller = activity_controller
        self._quitter = quitter

        self._image_acquirer = None  # type: Optional[ImageAcquirer]

    def init_session(self, image_acquirer: ImageAcquirer) -> None:
        self._image_acquirer = image_acquirer

    def back(self) -> None:
        from opendrop.app.start.component import StartComponent
        self._activity_controller.start_activity(StartComponent)

    def quit(self) -> None:
        self._quitter.quit()
