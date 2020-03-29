from typing import Type

from opendrop.app.common.core.imageacquirer import ImageAcquirerProvider
from opendrop.app.common.core.imageacquirer.filesystem import FilesystemAcquirerProvider
from opendrop.app.common.core.imageacquirer.usbcamera import USBCameraAcquirerProvider
from opendrop.appfw import WidgetComponent


class UnknownImageAcquirerProvider(Exception):
    """Raised when an unknown ImageAcquirerProvider is given to EditorResolver."""


class EditorResolver:
    @staticmethod
    def resolve(acquirer_provider: ImageAcquirerProvider) -> Type[WidgetComponent]:
        if isinstance(acquirer_provider, FilesystemAcquirerProvider):
            from .filesystem import FilesystemEditorComponent
            return FilesystemEditorComponent

        if isinstance(acquirer_provider, USBCameraAcquirerProvider):
            from .usbcamera import USBCameraEditorComponent
            return USBCameraEditorComponent

        raise UnknownImageAcquirerProvider('No editor found for {!r}'.format(acquirer_provider))
