from injector import Module, Binder

from ._abc import ImageAcquirerProvider, ImageAcquirer
from ._resolver import ImageAcquirerResolverModule, ImageAcquirerResolver
from .filesystem import FilesystemAcquirerModule, FilesystemAcquirerProvider, FilesystemAcquirer
from .usbcamera import USBCameraAcquirerModule, USBCameraAcquirerProvider, USBCameraAcquirer


class _AcquirersModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(FilesystemAcquirerModule)
        binder.install(USBCameraAcquirerModule)

        binder.install(ImageAcquirerResolverModule)
