from typing import Type, TypeVar

from injector import Injector, inject, Module, Binder, singleton

from ._base import ImageAcquirer, ImageAcquirerProvider

_ImageAcquirerT = TypeVar('_ImageAcquirerT', bound=ImageAcquirer)


class ImageAcquirerResolverModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=ImageAcquirerResolver, to=ImageAcquirerResolver, scope=singleton)


class ImageAcquirerResolver:
    @inject
    def __init__(self, injector: Injector) -> None:
        self._injector = injector

    def resolve(self, acquirer_cls: Type[_ImageAcquirerT]) -> ImageAcquirerProvider[_ImageAcquirerT]:
        return self._injector.get(ImageAcquirerProvider[acquirer_cls])
