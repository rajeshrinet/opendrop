from injector import Module, Binder, inject

from opendrop.app.service import AppService


class StartModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=StartService, to=StartService)


class StartService:
    @inject
    def __init__(self, app_service: AppService) -> None:
        self._app_service = app_service

    def new_ift_session(self) -> None:
        from opendrop.app.ift.component import IFTComponent
        self._app_service.start_activity(IFTComponent)

    def new_conan_session(self) -> None:
        print('new_conan_session()')

    def close(self) -> None:
        self._app_service.quit()
