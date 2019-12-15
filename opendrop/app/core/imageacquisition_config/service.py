from typing import Type, Optional, NewType, cast

from injector import Module, singleton, provider
from injector import inject, Injector

from opendrop.app.core.config_base import Configurator
from opendrop.app.core.imageacquisition.acquirers import (
    ImageAcquirer,
    ImageAcquirerProvider,
    FilesystemAcquirerProvider,
)
from opendrop.app.core.imageacquisition.service import ImageAcquisitionService
from opendrop.utility.bindable import VariableBindable
from opendrop.utility.bindable.typing import Bindable, ReadBindable


class ImageAcquisitionConfiguratorService(Configurator):
    @inject
    def __init__(self, service: ImageAcquisitionService, injector: Injector) -> None:
        self._service = service
        self._injector = injector

        self._acquirer_provider = VariableBindable(None)  # type: Bindable[Optional[ImageAcquirerProvider]]
        self.acquirer_provider = cast(ReadBindable[Optional[ImageAcquirerProvider]], self._acquirer_provider)

        self._prepared_acquirer = None  # type: Optional[ImageAcquirer]

    def change_provider_type(self, provider_cls: Type[ImageAcquirerProvider]) -> None:
        new_provider = self._injector.get(provider_cls)
        self._acquirer_provider.set(new_provider)

    def prepare(self) -> None:
        assert self._prepared_acquirer is None

        acquirer_provider = self.acquirer_provider.get()
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


_DefaultProviderType = NewType('_DefaultProviderType', Type[ImageAcquirerProvider])


class ImageAcquisitionConfiguratorModule(Module):
    @singleton
    @provider
    def service(self, injector: Injector, default_provider_type: _DefaultProviderType)\
            -> ImageAcquisitionConfiguratorService:
        default_provider_type = cast(Type[ImageAcquirerProvider], default_provider_type)

        service = injector.create_object(ImageAcquisitionConfiguratorService)
        service.change_provider_type(default_provider_type)

        return service

    @provider
    def default_provider_type(self) -> _DefaultProviderType:
        return cast(_DefaultProviderType, FilesystemAcquirerProvider)
