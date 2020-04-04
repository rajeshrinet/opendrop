import numpy as np
from injector import Module, Binder, singleton

from opendrop.utility.bindable.collections import BindableSet


class ImageStackServiceModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=ImageStackService, to=ImageStackService, scope=singleton)


class ImageStackService(BindableSet['ImageStackSlice']):
    pass


class ImageStackSlice:
    def __init__(self, timestamp: float, data: np.ndarray) -> None:
        self.timestamp = timestamp
        self.data = data
