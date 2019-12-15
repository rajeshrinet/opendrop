from typing import Generic, TypeVar


class ImageAcquirer:
    def destroy(self) -> None:
        """Destroy this object, releasing any resources no longer required."""


T = TypeVar('T', bound=ImageAcquirer)


class ImageAcquirerProvider(Generic[T]):
    def get(self) -> T:
        """Provide the ImageAcquirer object."""
