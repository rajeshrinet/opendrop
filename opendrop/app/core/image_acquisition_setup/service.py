from typing import Type, Optional, NewType, cast

from injector import Module, singleton, provider, Binder
from injector import inject, Injector

from opendrop.app.core.imageacquirer import (
    ImageAcquirersModule,
    ImageAcquirerResolver,
    ImageAcquirerProvider,
    ImageAcquirer,
    FilesystemAcquirer,
)
from opendrop.utility.bindable import VariableBindable
from opendrop.utility.bindable.typing import Bindable, ReadBindable

_DefaultAcquirerType = NewType('_DefaultAcquirerType', Type[ImageAcquirer])


class ImageAcquisitionSetupModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(ImageAcquirersModule)

    @singleton
    @provider
    def service(self, injector: Injector, default_acquirer_type: _DefaultAcquirerType)\
            -> 'ImageAcquisitionSetupService':
        default_acquirer_type = cast(Type[ImageAcquirer], default_acquirer_type)

        service = injector.create_object(ImageAcquisitionSetupService)
        service.change_acquirer_type(default_acquirer_type)

        return service

    @provider
    def default_acquirer_type(self) -> _DefaultAcquirerType:
        return cast(_DefaultAcquirerType, FilesystemAcquirer)


class ImageAcquisitionSetupService:
    @inject
    def __init__(self, resolver: ImageAcquirerResolver) -> None:
        self._resolver = resolver

        self._provider = VariableBindable(None)  # type: Bindable[Optional[ImageAcquirerProvider]]
        self.provider = cast(ReadBindable[Optional[ImageAcquirerProvider]], self._provider)

        self._prepared_acquirer = None  # type: Optional[ImageAcquirer]

    def change_acquirer_type(self, acquirer_cls: Type[ImageAcquirer]) -> None:
        new_provider = self._resolver.resolve(acquirer_cls)
        self._provider.set(new_provider)

    def get_acquirer(self) -> ImageAcquirer:
        assert self._prepared_acquirer is None

        acquirer_provider = self.provider.get()
        acquirer = acquirer_provider.get()

        return acquirer
