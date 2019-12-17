from typing import Optional

from injector import Module, Binder, inject, singleton

from opendrop.app.core.configurator import PreparationError
from opendrop.app.ift.core import SessionConfiguratorModule
from opendrop.app.ift.core.session_config_service import SessionConfiguratorService
from opendrop.app.ift.core.session_service import SessionService


class SetupModule(Module):
    def configure(self, binder: Binder):
        binder.install(SessionConfiguratorModule)
        binder.bind(interface=SetupService, to=SetupService, scope=singleton)


class SetupService:
    @inject
    def __init__(self, session_service: SessionService, config_service: SessionConfiguratorService) -> None:
        self._session_service = session_service
        self._config_service = config_service

    def set_up(self) -> Optional[Exception]:
        try:
            installer = self._config_service.prepare()
        except PreparationError as e:
            return e.cause
        else:
            installer.install(self._session_service)
