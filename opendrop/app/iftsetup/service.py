from injector import Module, Binder, inject, singleton

from opendrop.app.ift.component import IFTComponent
from opendrop.appfw import ActivityControllerService
from .session_factory import SessionFactoryModule, SessionFactoryService


class IFTSetupModule(Module):
    def configure(self, binder: Binder):
        binder.install(SessionFactoryModule)
        binder.bind(interface=IFTSetupService, to=IFTSetupService, scope=singleton)


class IFTSetupService:
    @inject
    def __init__(self, session_factory: SessionFactoryService, activity_controller: ActivityControllerService) -> None:
        self._session_factory = session_factory
        self._activity_controller = activity_controller

    def set_up(self) -> None:
        session = self._session_factory.create()
        self._activity_controller.start_activity(IFTComponent, session=session)
