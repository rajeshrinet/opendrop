from typing import Generic, TypeVar

T = TypeVar('T')


class ImageAcquirerProvider(Generic[T]):
    def get(self) -> T:
        """Provide the ImageAcquirer object."""
