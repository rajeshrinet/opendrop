from injector import inject

from opendrop.app.service import AppService


class IFTService:
    @inject
    def __init__(self, app_service: AppService) -> None:
        self._app_service = app_service

    def submit_setup(self) -> None:
        print('submit_setup()')

    def cancel_setup(self) -> None:
        self._app_service.show_start()

    def close_setup(self) -> None:
        self._app_service.quit()
