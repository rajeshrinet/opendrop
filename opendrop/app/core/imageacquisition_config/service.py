from typing import Type

from injector import inject, Injector

from opendrop.app.core.config_base import Configurator
from opendrop.app.core.imageacquisition.acquirers import ImageAcquirerProvider, FilesystemAcquirerProvider
from opendrop.app.core.imageacquisition.service import ImageAcquisitionService
from opendrop.utility.bindable import BoxBindable, Bindable


class ImageAcquisitionConfiguratorService(Configurator):
    @inject
    def __init__(self, service: ImageAcquisitionService, injector: Injector) -> None:
        self._service = service
        self._injector = injector

        self.acquirer_provider = BoxBindable(
            initial=self._resolve_default_acquirer_provider()
        )  # type: Bindable[ImageAcquirerProvider]

    def _resolve_default_acquirer_provider(self) -> ImageAcquirerProvider:
        provider = self._injector.get(FilesystemAcquirerProvider)
        return provider

    def change_provider(self, provider_cls: Type[ImageAcquirerProvider]) -> None:
        provider = self._injector.get(provider_cls)
        self.acquirer_provider.set(provider)

    def install(self) -> None:
        raise NotImplementedError