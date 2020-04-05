from gi.repository import Gtk
from injector import inject

from opendrop.app.common.core.imageacquirer import ImageAcquirer
from opendrop.app.common.observation.component import ObservationViewerComponent
from opendrop.appfw import Presenter, WidgetView, WidgetComponent, ComponentFactory
from .core.ift import IFTService


class IFTComponent(WidgetComponent):
    modules = []


@IFTComponent.view
class IFTComponentView(WidgetView):
    @inject
    def __init__(self, cf: ComponentFactory) -> None:
        root = Gtk.Grid()
        self.set_widget(root)

        observation_viewer = cf.create_widget(ObservationViewerComponent)
        root.add(observation_viewer)

        observation_viewer.props.hexpand = True
        observation_viewer.props.vexpand = True

        observation_viewer.show()


@IFTComponent.presenter
class IFTComponentPresenter(Presenter[IFTComponentView]):
    @inject
    def __init__(self, service: IFTService, *, image_acquirer: ImageAcquirer) -> None:
        self._service = service

        self._service.init_session(
            image_acquirer=image_acquirer,
        )
