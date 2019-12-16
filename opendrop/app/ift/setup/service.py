from typing import Optional

from injector import Module, Binder, inject, singleton

from opendrop.app.core.config import PreparationError
from opendrop.app.ift.core import SessionConfiguratorModule
from opendrop.app.ift.core.session_config_service import SessionConfiguratorService


class SetupModule(Module):
    def configure(self, binder: Binder):
        binder.install(SessionConfiguratorModule)
        binder.bind(interface=SetupService, to=SetupService, scope=singleton)


class SetupService:
    @inject
    def __init__(self, config: SessionConfiguratorService) -> None:
        self._config = config

    def set_up(self) -> Optional[Exception]:
        try:
            self._config.prepare()
        except PreparationError as e:
            self._config.reset()
            return e.cause
        else:
            self._config.install()
