from typing import Type, Optional

from injector import Module, Binder, singleton
from injector import inject, Injector

from opendrop.app.core.config_base import Configurator
from opendrop.app.core.imageacquisition.acquirers import ImageAcquirer, ImageAcquirerProvider, FilesystemAcquirerProvider
from opendrop.app.core.imageacquisition.service import ImageAcquisitionService
from opendrop.utility.bindable import VariableBindable
from opendrop.utility.bindable.typing import Bindable


class ImageAcquisitionConfiguratorModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=ImageAcquisitionConfiguratorService, to=ImageAcquisitionConfiguratorService, scope=singleton)


class ImageAcquisitionConfiguratorService(Configurator):
    @inject
    def __init__(self, service: ImageAcquisitionService, injector: Injector) -> None:
        self._service = service
        self._injector = injector

        self.acquirer_provider = VariableBindable(
            initial=self._resolve_default_acquirer_provider()
        )  # type: Bindable[ImageAcquirerProvider]

        self._prepared_acquirer = None  # type: Optional[ImageAcquirer]

    def _resolve_default_acquirer_provider(self) -> ImageAcquirerProvider:
        provider = self._injector.get(FilesystemAcquirerProvider)
        return provider

    def change_provider(self, provider_cls: Type[ImageAcquirerProvider]) -> None:
        provider = self._injector.get(provider_cls)
        self.acquirer_provider.set(provider)

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
