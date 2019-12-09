from injector import inject

from opendrop.app.ift.service import IFTService


class SetupService:
    @inject
    def __init__(self, ift_service: IFTService) -> None:
        self._ift_service = ift_service

    def submit(self) -> None:
        self._ift_service.submit_setup()

    def cancel(self) -> None:
        self._ift_service.cancel_setup()

    def close(self) -> None:
        self._ift_service.close_setup()
