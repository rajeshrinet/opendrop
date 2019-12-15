import math
from pathlib import Path
from typing import Sequence, Union

import numpy as np
from PIL import Image
from injector import Module, provider

from opendrop.utility.bindable import VariableBindable
from opendrop.utility.bindable.typing import Bindable
from ._abc import ImageAcquirerProvider


class EmptyPathsError(ValueError):
    """Raised when FilesystemAcquirer is given an empty image_paths."""


class UnknownImageTypeError(OSError):
    """Raised when trying to load an image of unknown type."""


class FilesystemAcquirerModule(Module):
    @provider
    def acquirer_provider(self) -> 'ImageAcquirerProvider[FilesystemAcquirer]':
        return FilesystemAcquirerProvider()


class FilesystemAcquirer:
    def __init__(self, image_paths: Sequence[Path], frame_interval: float) -> None:
        self._check_image_paths(image_paths)
        self._check_frame_interval(image_paths, frame_interval)

        self.images = [_load_image(path) for path in image_paths]
        self.frame_interval = frame_interval

    @staticmethod
    def _check_image_paths(image_paths: Sequence[Path]) -> None:
        if len(image_paths) == 0:
            raise EmptyPathsError("'image_paths' cannot be an empty sequence")

    @staticmethod
    def _check_frame_interval(image_paths: Sequence[Path], frame_interval: float) -> None:
        if len(image_paths) <= 1:
            return

        if not math.isfinite(frame_interval):
            raise ValueError("Expected 'frame_interval' to be finite, got '{}'".format(frame_interval))

        if frame_interval < 0:
            raise ValueError("'frame_interval' cannot be negative")


class FilesystemAcquirerProvider(ImageAcquirerProvider[FilesystemAcquirer]):
    def __init__(self) -> None:
        self.image_paths = VariableBindable(tuple())  # type: Bindable[Sequence[Path]]
        self.frame_interval = VariableBindable(math.nan)  # type: Bindable[float]

    def get(self) -> FilesystemAcquirer:
        image_paths = self.image_paths.get()
        frame_interval = self.frame_interval.get()

        return FilesystemAcquirer(
            image_paths=image_paths,
            frame_interval=frame_interval,
        )


def _load_image(path: Union[Path, str]) -> np.ndarray:
    try:
        image_pil = Image.open(path)
    except FileNotFoundError:
        raise
    except OSError as e:
        raise UnknownImageTypeError(str(e))

    image = np.array(image_pil)
    return image
