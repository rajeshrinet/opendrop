from typing import Type, TypeVar, Optional

from gi.repository import Gtk
from injector import Injector, inject, Module, Binder, UnsatisfiedRequirement

from .component import Component, _Component, WidgetComponent

ComponentT = TypeVar('ComponentT', bound=Component)


class _ComponentFactoryModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(ComponentFactory, to=ComponentFactory)


class ComponentFactory:
    @inject
    def __init__(self, injector: Injector) -> None:
        self._injector = injector

    def create(self, component_cls: Type[ComponentT], **kwargs) -> ComponentT:
        component = self._injector.create_object(
            cls=component_cls,
            additional_kwargs={'additional_kwargs': kwargs},
        )

        scope = self._scope
        if scope is not None:
            scope._register_child(component)
            component._parent = scope

        return component

    def create_widget(self, component_cls: Type[WidgetComponent], **kwargs) -> Gtk.Widget:
        component = self.create(component_cls, **kwargs)
        return component.widget

    @property
    def _scope(self) -> Optional[Component]:
        try:
            scope = self._injector.get(_Component)
        except UnsatisfiedRequirement:
            scope = None

        return scope
