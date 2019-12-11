from typing import Any


class ImageAcquisitionService:
    def __init__(self) -> None:
        self.is_ready = False
        self.acquirer = None

    def use_acquirer(self, acquirer: Any) -> None:
        self.acquirer = acquirer
        self.is_ready = True
