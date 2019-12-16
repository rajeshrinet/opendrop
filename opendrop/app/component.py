from typing import Optional, Type, Mapping, Any

from injector import inject

from opendrop.appfw import Component, View, Presenter, ComponentFactory, WidgetComponent
from .service import AppModule, AppService
from .start.component import StartComponent


class AppComponent(Component):
    modules = [AppModule]


@AppComponent.view
class AppView(View):
    @inject
    def __init__(self, cf: ComponentFactory) -> None:
        self._cf = cf
        self._activity = None  # type: Optional[Component]

    def _clear_activity(self) -> None:
        activity = self._activity
        if activity is None:
            return

        self._activity = None
        activity.destroy()

    def _set_activity(self, activity: Component) -> None:
        self._clear_activity()

        if activity is None:
            return

        self._activity = activity

    def start_activity(self, component_cls: Type[Component], kwargs: Mapping[str, Any]) -> None:
        component = self._cf.create(component_cls, **kwargs)
        self._set_activity(component)

        if isinstance(component, WidgetComponent):
            component.widget.show()


@AppComponent.presenter
class AppPresenter(Presenter):
    ENTRY_ACTIVITY = StartComponent

    @inject
    def __init__(self, service: AppService) -> None:
        self._service = service

        self._view = None  # type: Optional[AppView]
        self._before_view_destroy_cleanup_tasks = []

    def after_view_init(self, view: AppView) -> None:
        self._view = view

        connections = [
            self._service.on_start_activity.connect(self._hdl_start_activity),
        ]

        self._before_view_destroy_cleanup_tasks += (
            conn.disconnect
            for conn in connections
        )

        self._hdl_start_activity(self.ENTRY_ACTIVITY, {})

    def _hdl_start_activity(self, component_cls: Type[Component], kwargs: Mapping[str, Any]) -> None:
        self._view.start_activity(component_cls, kwargs)

    def before_view_destroy(self) -> None:
        for f in self._before_view_destroy_cleanup_tasks:
            f()
