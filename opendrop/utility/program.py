from abc import abstractmethod
from typing import Any

from injector import Injector


class Program:
    modules = []

    def __init__(self) -> None:
        self._injector = None

    def run(self, **kwargs) -> None:
        self._injector = Injector(
            modules=self.modules,
            auto_bind=False,
        )

        return self._injector.call_with_injection(self.main, kwargs=kwargs)

    @abstractmethod
    def main(self, *args, **kwargs) -> Any:
        """To be executed when program is run."""
