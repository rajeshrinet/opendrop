import sys
import time
import asyncio
import concurrent.futures
from typing import Optional

from ..camera import Camera
from ..protocol import Observation


PY_37 = sys.version_info >= (3, 7)


class CameraService:
    def __init__(self) -> None:
        self._initialized = False
        self._finalized = False

        self._camera = None  # type: Optional[Camera]
        self._cache = None  # type: Optional[concurrent.futures.Future[Observation]]

    def initialize(self, camera: Camera) -> None:
        assert not self._initialized
        assert not self._finalized
        assert self._camera is None

        self._camera = camera

    async def capture(self, max_age: float = 0.0) -> Observation:
        current_cache = self._cache

        if current_cache is None or max_age == 0.0:
            self._refresh_cache()
        elif current_cache.done() and current_cache.exception():
            self._refresh_cache()
        elif current_cache.done() and not current_cache.exception():
            observation = current_cache.result()
            now = time.time()
            if max_age > 0 and observation.timestamp < now - max_age:
                self._refresh_cache()

        assert self._cache is not None

        running_loop = asyncio.get_running_loop() if PY_37 else asyncio.get_event_loop()
        observation = await asyncio.wrap_future(self._cache, loop=running_loop)

        return observation

    def _refresh_cache(self) -> None:
        assert self._camera is not None

        fut = concurrent.futures.Future()
        fut.set_running_or_notify_cancel()

        self._camera.read(
                success_cb=lambda image, timestamp:
                    fut.set_result(Observation(image, timestamp, is_replicated=False)),
                exception_cb=fut.set_exception,
        )

        self._cache = fut

    def finalize(self) -> None:
        assert self._initialized

        if self._finalized:
            return

        self._finalized = True
        self._camera = None
