import time
from typing import Optional, Tuple
import cv2
import numpy as np
from .protocol import Camera, CameraException


class OpenCVCamera(Camera):
    def __init__(self, index: int) -> None:
        self._vc = cv2.VideoCapture(index)

    def capture(self, expire: Optional[float] = None) -> Tuple[np.ndarray, float]:
        success, image = self._vc.read()
        timestamp = time.time()
        if not success:
            raise CameraException

        image.flags.writeable = False

        return image, timestamp

    def destroy(self) -> None:
        self._vc.release()
