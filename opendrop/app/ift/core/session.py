from injector import inject

from opendrop.app.core.imageacquirer import ImageAcquirer


class SessionService:
    @inject
    def __init__(self, image_acquirer: ImageAcquirer) -> None:
        self.image_acquirer = image_acquirer
