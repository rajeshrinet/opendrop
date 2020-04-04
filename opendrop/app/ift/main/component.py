from gi.repository import Gtk
from injector import inject

from opendrop.app.common.observation.component import ObservationViewerComponent
from opendrop.appfw import Presenter, WidgetView, WidgetComponent, ComponentFactory


class IFTMainComponent(WidgetComponent):
    modules = []


@IFTMainComponent.view
class IFTMainView(WidgetView):
    @inject
    def __init__(self, cf: ComponentFactory) -> None:
        root = Gtk.Grid()
        self.set_widget(root)

        observation_viewer = cf.create_widget(ObservationViewerComponent)
        root.add(observation_viewer)

        observation_viewer.props.hexpand = True
        observation_viewer.props.vexpand = True

        observation_viewer.show()


@IFTMainComponent.presenter
class IFTMainPresenter(Presenter[IFTMainView]):
    pass
