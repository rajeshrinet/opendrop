from injector import Module, provider

from ._abc import ImageAcquirerProvider, ImageAcquirer


class USBCameraAcquirerModule(Module):
    @provider
    def acquirer_provider(self) -> 'ImageAcquirerProvider[USBCameraAcquirer]':
        return USBCameraAcquirerProvider()


class USBCameraAcquirer(ImageAcquirer):
    pass


class USBCameraAcquirerProvider(ImageAcquirerProvider[USBCameraAcquirer]):
    def get(self) -> USBCameraAcquirer:
        raise NotImplementedError
