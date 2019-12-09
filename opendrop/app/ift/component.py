from typing import Optional

from injector import Module, Binder, inject, singleton

from opendrop.appfw import Component, View, Presenter, ComponentFactory
from .core import IFTSessionModule
from .service import IFTService
from .setup.component import SetupComponent


class IFTModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.install(IFTSessionModule)
        binder.bind(interface=IFTService, to=IFTService, scope=singleton)


class IFTComponent(Component):
    modules = [IFTModule]


@IFTComponent.view
class IFTView(View):
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

    def show_setup(self) -> None:
        setup_cmp = self._cf.create(SetupComponent)
        self._set_activity(setup_cmp)
        setup_cmp.widget.show()


@IFTComponent.presenter
class IFTPresenter(Presenter[IFTView]):
    @inject
    def __init__(self, service: IFTService) -> None:
        self._service = service

    def after_view_init(self, view: IFTView) -> None:
        view.show_setup()
