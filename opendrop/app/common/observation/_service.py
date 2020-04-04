from injector import Module, Binder, singleton


class ObservationViewerServiceModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=ObservationViewerService, to=ObservationViewerService, scope=singleton)


class ObservationViewerService:
    pass
