from inspect import Signature, Parameter, signature
from typing import Mapping, Any, MutableSequence, Callable, Iterator, Sequence, Optional, Type, NewType, cast

from injector import Injector, Binder, CallableProvider, Module, InstanceProvider, inject

from opendrop.utility.events import Event
from .presenter import Presenter
from .view import View, WidgetView


class Component:
    modules = ()  # type: Sequence

    _view_cls = None  # type: Optional[Type[View]]
    _presenter_cls = None  # type: Optional[Type[Presenter]]

    @inject
    def __init__(self, parent_injector: Injector, *, additional_kwargs: Mapping[str, Any]) -> None:
        self._children_registry = ComponentChildrenRegistry()
        self._parent = None  # type: Optional[Component]
        self._is_destroyed = False

        self.on_destroyed = Event()

        # Create a new child injector for this component.
        self._injector = Injector(
            modules=[*self.modules, _ComponentContextModule(self)],
            parent=parent_injector,
            auto_bind=False,
        )

        assert self._presenter_cls is not None

        presenter_kwargs = _filter_kwargs(
            signature=signature(self._presenter_cls.__init__),
            kwargs=additional_kwargs,
        )

        view_kwargs = _filter_kwargs(
            signature=signature(self._view_cls.__init__),
            kwargs=additional_kwargs,
        )

        unused_keywords = set(additional_kwargs.keys()) - {*presenter_kwargs.keys(), *view_kwargs.keys()}
        if unused_keywords:
            raise ValueError("'additional_kwargs' contains unused keywords {!s}".format(unused_keywords))

        self._presenter_obj = self._injector.create_object(
            cls=self._presenter_cls,
            additional_kwargs=presenter_kwargs
        )

        assert self._view_cls is not None

        self._view_obj = self._injector.create_object(
            cls=self._view_cls,
            additional_kwargs=_filter_kwargs(
                signature=signature(self._view_cls.__init__),
                kwargs=additional_kwargs
            ),
        )

        self._presenter_obj.after_view_init(self._view_obj)

    def _register_child(self, child: 'Component') -> None:
        self._children_registry.register(child)

    def destroy(self) -> None:
        if self._is_destroyed:
            raise ValueError('{} is already destroyed'.format(self))

        self._is_destroyed = True
        self.on_destroyed.fire()

        for child in self._children_registry:
            child.destroy()

        self._presenter_obj.before_view_destroy()
        self._view_obj.destroy()
        self._presenter_obj.destroy()

        self._parent = None

    @classmethod
    def presenter(cls, presenter_cls: Type[Presenter]) -> Type[Presenter]:
        cls._presenter_cls = presenter_cls
        return presenter_cls

    @classmethod
    def view(cls, view_cls: Type[View]) -> Type[View]:
        cls._view_cls = view_cls
        return view_cls


class ComponentChildrenRegistry:
    class ChildWatcher:
        def __init__(self, child: Component, on_child_destroyed: Callable) -> None:
            self._child_destroyed_callback = on_child_destroyed
            self.child = child

            on_child_destroyed_conn = self.child.on_destroyed.connect(self._hdl_child_destroyed)

            self._cleanup_tasks = [
                on_child_destroyed_conn.disconnect
            ]  # type: Sequence[Callable]

        def _hdl_child_destroyed(self) -> None:
            self._child_destroyed_callback(self)

        def destroy(self) -> None:
            for f in self._cleanup_tasks:
                f()

    def __init__(self) -> None:
        self._watchers = []  # type: MutableSequence[ComponentChildrenRegistry.ChildWatcher]

    def register(self, child: Component) -> None:
        watcher = self.ChildWatcher(child, on_child_destroyed=self._deregister)
        self._watchers.append(watcher)

    def _deregister(self, watcher: ChildWatcher) -> None:
        assert watcher in self._watchers
        self._watchers.remove(watcher)
        watcher.destroy()

    def __iter__(self) -> Iterator[Component]:
        return (
            watcher.child for watcher in tuple(self._watchers)
        )


_Component = NewType('_Component', Component)


class _ComponentContextModule(Module):
    def __init__(self, component: Component) -> None:
        self._component = component

    def configure(self, binder: Binder) -> None:
        binder.bind(
            interface=_Component,
            to=InstanceProvider(self._component)
        )

        binder.bind(
            interface=self._component._presenter_cls,
            to=CallableProvider(lambda: self._component._presenter_obj)
        )


class WidgetComponent(Component):
    @inject
    def __init__(self, parent_injector: Injector, **kwargs) -> None:
        super().__init__(
            parent_injector=parent_injector,
            **kwargs
        )

        widget = cast(WidgetView, self._view_obj)._widget
        assert widget is not None

        self.widget = widget

    def destroy(self) -> None:
        super().destroy()

        self.widget.destroy()


def _filter_kwargs(signature: Signature, kwargs: Mapping) -> Mapping:
    if any(param.kind is Parameter.VAR_KEYWORD for param in signature.parameters.values()):
        return kwargs

    kwargs = {
        k: v
        for k, v in kwargs.items()
        if k in signature.parameters
    }

    kwargs = {
        k: v
        for k, v in kwargs.items()
        if signature.parameters[k].kind is Parameter.POSITIONAL_OR_KEYWORD or
           signature.parameters[k].kind is Parameter.KEYWORD_ONLY
    }

    return kwargs
