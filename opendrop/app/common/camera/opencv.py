import time
from typing import Optional, Tuple, Callable, Any

import concurrent.futures
import numpy as np

import cv2

from .protocol import Camera, CameraException


class OpenCVCamera(Camera):
    class _ReaderDoneCallback:
        def __init__(self, success_cb: Callable[[np.ndarray, float], Any], exception_cb: Callable[[Exception], Any]):
            self._success_cb = success_cb
            self._exception_cb = exception_cb

        def __call__(self, fut: concurrent.futures.Future):
            try:
                image, timestamp = fut.result()
                self._success_cb(image, timestamp)
            except Exception as e:
                self._exception_cb(e)

    def __init__(self, index: int) -> None:
        self._vc = cv2.VideoCapture(index)
        self._thread_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._active_reader = None  # type: Optional[concurrent.futures.Future]

    def read(self, success_cb: Callable[[np.ndarray, float], Any], exception_cb: Callable[[Exception], Any]) -> None:
        if self._active_reader is None or self._active_reader.done():
            self._active_reader = self._thread_executor.submit(self._reader, self._vc)

        self._active_reader.add_done_callback(
                self._ReaderDoneCallback(success_cb, exception_cb)
        )
        
    @staticmethod
    def _reader(vc: cv2.VideoCapture) -> Tuple[np.ndarray, float]:
        success, image = vc.read()
        timestamp = time.time()
        if not success:
            raise CameraException

        image.flags.writeable = False

        return image, timestamp

    def destroy(self) -> None:
        self._thread_executor.shutdown(wait=True)
        self._vc.release()
