from abc import abstractmethod
from typing import Any

from injector import Injector, Binder


class Program:
    modules = []

    def __init__(self) -> None:
        self._injector = None

    def run(self, **kwargs) -> None:
        self._injector = Injector(
            modules=[*self.modules, self.configure],
            auto_bind=False,
        )

        return self._injector.call_with_injection(self.main, kwargs=kwargs)

    def configure(self, binder: Binder) -> None:
        """Additional module to be installed into injector."""

    @abstractmethod
    def main(self, *args, **kwargs) -> Any:
        """To be executed when program is run."""
