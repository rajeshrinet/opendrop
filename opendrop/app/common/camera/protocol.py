from abc import abstractmethod
from typing import Optional, Tuple

import numpy as np


class CameraException(Exception):
    """Base class for exceptions that can be raised by Camera."""


class Camera:
    @abstractmethod
    def capture(self, expire: Optional[float] = None) -> Tuple[np.ndarray, float]:
        """Return (image, timestamp) pair."""

    def destroy(self) -> None:
        """Destroy this and release any resources."""
