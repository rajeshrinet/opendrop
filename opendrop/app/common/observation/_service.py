from injector import Module, Binder, singleton


class ObservationViewerComponentServiceModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=ObservationViewerComponentService, to=ObservationViewerComponentService, scope=singleton)


class ObservationViewerComponentService:
    pass
