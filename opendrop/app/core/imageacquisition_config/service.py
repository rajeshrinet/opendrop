from typing import Type, Optional, NewType, cast

from injector import Module, singleton, provider, Binder
from injector import inject, Injector

from opendrop.app.core.config import Configurator, PreparationError, Installer
from opendrop.app.core.imageacquisition.acquirers import (
    ImageAcquirersModule,
    ImageAcquirerResolver,
    ImageAcquirerProvider,
    ImageAcquirer,
    FilesystemAcquirer,
)
from opendrop.app.core.imageacquisition.service import ImageAcquisitionService
from opendrop.utility.bindable import VariableBindable
from opendrop.utility.bindable.typing import Bindable, ReadBindable


class ImageAcquisitionConfiguratorService(Configurator[ImageAcquisitionService]):
    @inject
    def __init__(self, resolver: ImageAcquirerResolver) -> None:
        self._resolver = resolver

        self._provider = VariableBindable(None)  # type: Bindable[Optional[ImageAcquirerProvider]]
        self.provider = cast(ReadBindable[Optional[ImageAcquirerProvider]], self._provider)

        self._prepared_acquirer = None  # type: Optional[ImageAcquirer]

    def change_acquirer_type(self, acquirer_cls: Type[ImageAcquirer]) -> None:
        new_provider = self._resolver.resolve(acquirer_cls)
        self._provider.set(new_provider)

    def prepare(self) -> 'ImageAcquisitionInstaller':
        assert self._prepared_acquirer is None

        acquirer_provider = self.provider.get()

        try:
            prepared_acquirer = acquirer_provider.get()
        except Exception as e:
            raise PreparationError(cause=e)

        return ImageAcquisitionInstaller(prepared_acquirer)


class ImageAcquisitionInstaller(Installer[ImageAcquisitionService]):
    def __init__(self, acquirer: ImageAcquirer) -> None:
        self._acquirer = acquirer

    def install(self, target: ImageAcquisitionService) -> None:
        if self._acquirer is None:
            raise ValueError('Installer has already been used')

        target.use_acquirer(self._acquirer)
        self._acquirer = None

    def destroy(self) -> None:
        if self._acquirer is None:
            return

        self._acquirer.destroy()
        self._acquirer = None


_DefaultAcquirerType = NewType('_DefaultAcquirerType', Type[ImageAcquirer])


class ImageAcquisitionConfiguratorModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(ImageAcquirersModule)

    @singleton
    @provider
    def service(self, injector: Injector, default_acquirer_type: _DefaultAcquirerType)\
            -> ImageAcquisitionConfiguratorService:
        default_acquirer_type = cast(Type[ImageAcquirer], default_acquirer_type)

        service = injector.create_object(ImageAcquisitionConfiguratorService)
        service.change_acquirer_type(default_acquirer_type)

        return service

    @provider
    def default_acquirer_type(self) -> _DefaultAcquirerType:
        return cast(_DefaultAcquirerType, FilesystemAcquirer)
