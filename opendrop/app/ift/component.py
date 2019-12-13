from typing import Optional

from injector import inject

from opendrop.appfw import Component, View, Presenter, ComponentFactory
from . import IFTModule
from .service import IFTService
from .setup.component import SetupComponent


class IFTComponent(Component):
    modules = [IFTModule]


@IFTComponent.view
class IFTView(View):
    @inject
    def __init__(self, presenter: 'IFTPresenter', cf: ComponentFactory) -> None:
        self._presenter = presenter
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
        setup_cmp = self._cf.create(
            SetupComponent,
            on_success=self._presenter.hdl_setup_success,
            on_cancel=self._presenter.hdl_setup_cancel,
            on_close=self._presenter.hdl_setup_close,
        )
        self._set_activity(setup_cmp)
        setup_cmp.widget.show()


@IFTComponent.presenter
class IFTPresenter(Presenter[IFTView]):
    @inject
    def __init__(self, service: IFTService) -> None:
        self._service = service

    def after_view_init(self, view: IFTView) -> None:
        view.show_setup()

    def hdl_setup_success(self) -> None:
        print('setup success')

    def hdl_setup_cancel(self) -> None:
        self._service.back()

    def hdl_setup_close(self) -> None:
        self._service.quit()
