from injector import Module, provider

from ._abc import ImageAcquirerProvider


class USBCameraAcquirerModule(Module):
    @provider
    def acquirer_provider(self) -> 'ImageAcquirerProvider[USBCameraAcquirer]':
        return USBCameraAcquirerProvider()


class USBCameraAcquirer:
    pass


class USBCameraAcquirerProvider(ImageAcquirerProvider[USBCameraAcquirer]):
    def get(self) -> USBCameraAcquirer:
        raise NotImplementedError
