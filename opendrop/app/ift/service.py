from typing import Optional

from injector import Module, Binder, inject, singleton, provider

from opendrop.app.core.imageacquirer import ImageAcquirer
from opendrop.appfw import ActivityControllerService, QuitService
from .core.session import SessionService


class IFTModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=IFTService, to=IFTService, scope=singleton)

    @provider
    def session(self, root: 'IFTService') -> SessionService:
        session = root._session
        assert session is not None
        return session

    @provider
    def image_acquirer(self, session: SessionService) -> ImageAcquirer:
        return session.image_acquirer


class IFTService:
    @inject
    def __init__(self, activity_controller: ActivityControllerService, quitter: QuitService) -> None:
        self._activity_controller = activity_controller
        self._quitter = quitter
        self._session = None  # type: Optional[SessionService]

    def set_session(self, session: SessionService) -> None:
        assert self._session is None
        self._session = session

    def back(self) -> None:
        from opendrop.app.start.component import StartComponent
        self._activity_controller.start_activity(StartComponent)

    def quit(self) -> None:
        self._quitter.quit()
