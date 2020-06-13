from abc import abstractmethod
from typing import Callable, Any

import numpy as np


class CameraException(Exception):
    """Base class for exceptions that can be raised by Camera."""


class Camera:
    @abstractmethod
    def read(self, success_cb: Callable[[np.ndarray, float], Any], exception_cb: Callable[[Exception], Any]) -> None:
        """Read a frame from the camera (ideally from a different thread) and invoke success_cb with the
        (image, timestamp) pair, otherwise invoke exception_cb with any exception that ocurred. It is not
        necessary to invoke the callbacks from the same thread as this function was called in, but they must
        be invoked in the same process."""

    def destroy(self) -> None:
        """Destroy this and release any resources."""
