from injector import Module, provider

from .base import ImageAcquirerProvider


class USBCameraAcquirer:
    pass


class USBCameraAcquirerProvider(ImageAcquirerProvider[USBCameraAcquirer]):
    def get(self) -> USBCameraAcquirer:
        raise NotImplementedError


class USBCameraAcquirerModule(Module):
    @provider
    def acquirer_provider(self) -> USBCameraAcquirerProvider:
        return USBCameraAcquirerProvider()
