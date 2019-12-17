from injector import Injector, inject, Module, Binder, singleton

from opendrop.app.core.image_acquisition_setup.service import ImageAcquisitionSetupModule, ImageAcquisitionSetupService
from opendrop.app.ift.core.session import SessionService


class SessionFactoryModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(ImageAcquisitionSetupModule)
        binder.bind(interface=SessionFactoryService, to=SessionFactoryService, scope=singleton)


class SessionFactoryService:
    @inject
    def __init__(self, injector: Injector, image_acquisition_setup: ImageAcquisitionSetupService) -> None:
        self._injector = injector
        self._image_acquisition_setup = image_acquisition_setup

    def create(self) -> SessionService:
        parts = {}

        try:
            parts['image_acquirer'] = self._image_acquisition_setup.get_acquirer()
        except Exception:
            for part in parts.values():
                part.destroy()
            raise

        session = self._injector.create_object(SessionService, additional_kwargs=parts)

        return session
