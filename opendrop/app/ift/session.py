from injector import inject

from opendrop.app.common.core.imageacquirer import ImageAcquirer


class IFTSession:
    @inject
    def __init__(self, image_acquirer: ImageAcquirer) -> None:
        self.image_acquirer = image_acquirer
