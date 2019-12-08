from injector import inject

from opendrop.app.service import AppService


class StartService:
    @inject
    def __init__(self, app_service: AppService) -> None:
        self._app_service = app_service

    def new_ift_session(self) -> None:
        self._app_service.new_ift_session()

    def new_conan_session(self) -> None:
        self._app_service.new_conan_session()

    def close(self) -> None:
        self._app_service.quit()
