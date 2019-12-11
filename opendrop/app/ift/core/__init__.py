from injector import Module, Binder, singleton

from opendrop.app.core.imageacquisition import ImageAcquisitionModule
from opendrop.app.core.imageacquisition_config import ImageAcquisitionConfiguratorModule
from .service import IFTSessionService


class IFTSessionModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(ImageAcquisitionModule)
        binder.install(ImageAcquisitionConfiguratorModule)

        binder.bind(interface=IFTSessionService, to=IFTSessionService, scope=singleton)
