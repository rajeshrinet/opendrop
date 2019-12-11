from injector import inject

from opendrop.app.core.imageacquisition import ImageAcquisitionService


class IFTSessionService:
    @inject
    def __init__(self, image_acquisition_service: ImageAcquisitionService) -> None:
        self._image_acquisition_service = image_acquisition_service
