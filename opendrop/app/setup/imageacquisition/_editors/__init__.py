from injector import Module, Binder
from .resolver import EditorResolver


class EditorsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=EditorResolver, to=EditorResolver)
