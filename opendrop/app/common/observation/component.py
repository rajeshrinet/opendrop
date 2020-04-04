from gi.repository import Gtk

from opendrop.appfw import WidgetComponent, WidgetView, Presenter
from ._service import ObservationViewerServiceModule


class ObservationViewerComponent(WidgetComponent):
    modules = [ObservationViewerServiceModule]


@ObservationViewerComponent.view
class ObservationViewerView(WidgetView):
    def __init__(self) -> None:
        root = Gtk.AspectFrame(ratio=1, obey_child=False)
        self.set_widget(root)

        root.add(Gtk.Label('Observation Viewer', visible=True))


@ObservationViewerComponent.presenter
class ObservationViewerPresenter(Presenter[ObservationViewerView]):
    def __init__(self) -> None:
        pass
