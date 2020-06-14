import numpy as np


class Observation:
    def __init__(self, image: np.ndarray, timestamp: float, is_replicated: bool) -> None:
        assert not image.flags.writeable
        self._image = image
        self._timestamp = timestamp
        self._is_replicated = is_replicated

    @property
    def image(self) -> np.ndarray:
        return self._image

    @property
    def timestamp(self) -> float:
        return self._timestamp

    @property
    def is_replicated(self) -> bool:
        return self._is_replicated
