from injector import Module, provider

from .base import ImageAcquirerProvider


class FilesystemAcquirer:
    pass


class FilesystemAcquirerProvider(ImageAcquirerProvider[FilesystemAcquirer]):
    def get(self) -> FilesystemAcquirer:
        return FilesystemAcquirer()


class FilesystemAcquirerModule(Module):
    @provider
    def acquirer_provider(self) -> FilesystemAcquirerProvider:
        return FilesystemAcquirerProvider()
