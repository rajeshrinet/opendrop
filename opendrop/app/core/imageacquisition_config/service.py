from typing import Type, Optional, NewType, cast

from injector import Module, singleton, provider
from injector import inject, Injector

from opendrop.app.core.config_abc import Configurator
from opendrop.app.core.imageacquisition.acquirers import (
    ImageAcquirer,
    ImageAcquirerResolver,
    ImageAcquirerProvider,
    FilesystemAcquirer
)
from opendrop.app.core.imageacquisition.service import ImageAcquisitionService
from opendrop.utility.bindable import VariableBindable
from opendrop.utility.bindable.typing import Bindable, ReadBindable


class ImageAcquisitionConfiguratorService(Configurator):
    @inject
    def __init__(self, service: ImageAcquisitionService, resolver: ImageAcquirerResolver) -> None:
        self._service = service
        self._resolver = resolver

        self._provider = VariableBindable(None)  # type: Bindable[Optional[ImageAcquirerProvider]]
        self.provider = cast(ReadBindable[Optional[ImageAcquirerProvider]], self._provider)

        self._prepared_acquirer = None  # type: Optional[ImageAcquirer]

    def change_acquirer_type(self, acquirer_cls: Type[ImageAcquirer]) -> None:
        new_provider = self._resolver.resolve(acquirer_cls)
        self._provider.set(new_provider)

    def prepare(self) -> None:
        assert self._prepared_acquirer is None

        acquirer_provider = self.provider.get()
        self._prepared_acquirer = acquirer_provider.get()

    def reset(self) -> None:
        if self._prepared_acquirer is None:
            return

        prepared_acquirer = self._prepared_acquirer
        self._prepared_acquirer = None
        prepared_acquirer.destroy()

    def install(self) -> None:
        assert self._prepared_acquirer is not None

        prepared_acquirer = self._prepared_acquirer
        self._prepared_acquirer = None
        self._service.use_acquirer(prepared_acquirer)


_DefaultAcquirerType = NewType('_DefaultAcquirerType', Type[ImageAcquirer])


class ImageAcquisitionConfiguratorModule(Module):
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
