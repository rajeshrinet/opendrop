class PreparationError(Exception):
    def __init__(self, *args, cause: Exception) -> None:
        super().__init__(*args)
        self.cause = cause


class Configurator:
    def prepare(self) -> None:
        pass

    def reset(self) -> None:
        pass

    def install(self) -> None:
        pass
