import math
from pathlib import Path
from typing import Sequence

import cv2
from injector import Module, provider

from opendrop.utility.bindable import BoxBindable, Bindable
from .base import ImageAcquirerProvider


class FilesystemAcquirer:
    def __init__(self, image_paths: Sequence[Path], frame_interval: float) -> None:
        if len(image_paths) == 0:
            raise ValueError("'image_paths' cannot be an empty sequence")

        if len(image_paths) > 1 and not math.isfinite(frame_interval):
            raise ValueError("Expected 'frame_interval' to be finite, got '{}'".format(frame_interval))

        self.images = []
        for image_path in image_paths:
            image = cv2.imread(str(image_path), flags=cv2.IMREAD_COLOR)
            self.images.append(image)

        self.frame_interval = frame_interval


class FilesystemAcquirerProvider(ImageAcquirerProvider[FilesystemAcquirer]):
    def __init__(self) -> None:
        self.image_paths = BoxBindable(initial=())  # type: Bindable[Sequence[Path]]
        self.frame_interval = BoxBindable(initial=math.nan)  # type: Bindable[float]

    def get(self) -> FilesystemAcquirer:
        image_paths = self.image_paths.get()
        frame_interval = self.frame_interval.get()

        return FilesystemAcquirer(
            image_paths=image_paths,
            frame_interval=frame_interval,
        )


class FilesystemAcquirerModule(Module):
    @provider
    def acquirer_provider(self) -> FilesystemAcquirerProvider:
        return FilesystemAcquirerProvider()
