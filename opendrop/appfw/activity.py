from typing import Optional, Type, Mapping, Any, Sequence

from injector import Binder, Module, inject, singleton

from .component import Component, WidgetComponent
from .component_factory import ComponentFactory
from .presenter import Presenter
from .view import View


class _ActivityControllerModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=ActivityControllerService, to=ActivityControllerService, scope=singleton)


class ActivityControllerService:
    @inject
    def __init__(self) -> None:
        self._do_start_activity = None

    def start_activity(self, component_cls: Type[Component], **kwargs) -> None:
        self._do_start_activity(component_cls, kwargs)


def activitycontroller(
        entry: Type[Component],
        entry_kwargs: Optional[Mapping[str, Any]] = None,
        core_modules: Optional[Sequence] = None
) -> Type[Component]:
    entry_kwargs = entry_kwargs or {}
    core_modules = core_modules or []

    class ActivityControllerComponent(Component):
        modules = [_ActivityControllerModule, *core_modules]

    @ActivityControllerComponent.view
    class ActivityControllerView(View):
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

        def _set_activity(self, activity: Optional[Component]) -> None:
            self._clear_activity()

            if activity is None:
                return

            self._activity = activity

        def start_activity(self, component_cls: Type[Component], kwargs: Mapping[str, Any]) -> None:
            component = self._cf.create(component_cls, **kwargs)
            self._set_activity(component)

            if isinstance(component, WidgetComponent):
                component.widget.show()

    @ActivityControllerComponent.presenter
    class ActivityControllerPresenter(Presenter[ActivityControllerView]):
        @inject
        def __init__(self, service: ActivityControllerService) -> None:
            self._service = service

            self._view = None  # type: Optional[ActivityControllerView]
            self._before_view_destroy_cleanup_tasks = []

        def after_view_init(self, view: ActivityControllerView) -> None:
            self._view = view
            self._service._do_start_activity = self._start_activity

            self._start_activity(entry, entry_kwargs)

        def _start_activity(self, component_cls: Type[Component], kwargs: Mapping[str, Any]) -> None:
            self._view.start_activity(component_cls, kwargs)

        def before_view_destroy(self) -> None:
            self._service._do_start_activity = None

    return ActivityControllerComponent
