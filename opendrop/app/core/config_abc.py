from typing import Type, Union


class PreparationError(Exception):
    def __init__(self, *args, cause: Union[Exception, Type[Exception]]) -> None:
        super().__init__(*args)
        self.cause = cause


class Configurator:
    def prepare(self) -> None:
        pass

    def reset(self) -> None:
        pass

    def install(self) -> None:
        pass
