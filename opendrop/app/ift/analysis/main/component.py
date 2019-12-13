from gi.repository import Gtk

from opendrop.appfw import WidgetComponent, WidgetView, Presenter


class MainComponent(WidgetComponent):
    pass


@MainComponent.view
class MainView(WidgetView):
    def __init__(self) -> None:
        window = Gtk.Window(title='Interfacial Tension')
        self.set_widget(window)


@MainComponent.presenter
class MainPresenter(Presenter):
    pass
