import numpy as np

from opendrop.utility.bindable.collections import BindableSet


class ImageStack(BindableSet['ImageStackSlice']):
    pass


class ImageStackSlice:
    def __init__(self, timestamp: float, data: np.ndarray) -> None:
        self.timestamp = timestamp
        self.data = data
