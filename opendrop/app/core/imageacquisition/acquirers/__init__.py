from injector import Module, Binder

from ._base import ImageAcquirerProvider, ImageAcquirer
from .filesystem import FilesystemAcquirerModule, FilesystemAcquirerProvider, FilesystemAcquirer
from .usbcamera import USBCameraAcquirerModule, USBCameraAcquirerProvider, USBCameraAcquirer


class _AcquirersModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(FilesystemAcquirerModule)
        binder.install(USBCameraAcquirerModule)
