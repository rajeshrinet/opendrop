from abc import abstractmethod
from typing import Generic, TypeVar, Type, get_type_hints, Tuple


class ImageAcquirer:
    @property
    def size(self) -> Tuple[int, int]:
        """The (width, height) of images that are acquired."""

    def destroy(self) -> None:
        """Destroy this object, releasing any resources no longer required."""


T = TypeVar('T', bound=ImageAcquirer)


class ImageAcquirerProvider(Generic[T]):
    @abstractmethod
    def get(self) -> T:
        """Provide the ImageAcquirer object."""

    @property
    def provides(self) -> Type[T]:
        annotations = get_type_hints(self.get)
        return annotations['return']
