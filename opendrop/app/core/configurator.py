from abc import abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class PreparationError(Exception):
    def __init__(self, *args, cause: Exception) -> None:
        super().__init__(*args)
        self.cause = cause


class Configurator(Generic[T]):
    @abstractmethod
    def prepare(self) -> 'Installer[T]':
        pass


class Installer(Generic[T]):
    def install(self, target: T) -> None:
        pass

    def destroy(self) -> None:
        pass
