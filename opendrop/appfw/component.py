from inspect import Parameter, Signature, signature
import warnings
from typing import (
    Any,
    Callable,
    Iterator,
    Mapping,
    MutableSequence,
    NewType,
    Optional,
    Sequence,
    Type,
    TypeVar,
    cast,
)

from gi.repository import Gtk
from injector import (
    Binder,
    CallableProvider,
    Injector,
    InstanceProvider,
    Module,
    inject,
)

from opendrop.utility.events import Event

from .presenter import Presenter
from .view import View, WidgetView

PresenterT = TypeVar('PresenterT', bound=Presenter)
ViewT = TypeVar('ViewT', bound=View)


class Component:
    modules = ()  # type: Sequence

    _view_cls = None  # type: Optional[Type]
    _presenter_cls = None  # type: Optional[Type]

    @inject
    def __init__(
            self,
            parent_injector: Optional[Injector] = None,
            *,
            additional_kwargs: Optional[Mapping[str, Any]] = None
    ) -> None:
        additional_kwargs = additional_kwargs or {}

        self._children_registry = ComponentChildrenRegistry()
        self._parent = None  # type: Optional[Component]
        self._is_initialised = False
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
            raise TypeError("'additional_kwargs' contains unused keywords {!s}".format(unused_keywords))

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

        # Mark component as initialised
        self._is_initialised = True

    def _register_child(self, child: 'Component') -> None:
        self._children_registry.register(child)

    def destroy(self) -> None:
        if not self._is_initialised:
            raise ValueError("Can't destroy this component as it is not yet fully initialised.")

        if self._is_destroyed:
            return

        self._is_destroyed = True
        self.on_destroyed.fire()

        for child in self._children_registry:
            child.destroy()

        self._presenter_obj.before_view_destroy()
        self._view_obj.destroy()
        self._presenter_obj.destroy()

        self._parent = None

    @classmethod
    def presenter(cls, presenter_cls: Type[PresenterT]) -> Type[PresenterT]:
        cls._presenter_cls = presenter_cls
        return presenter_cls

    @classmethod
    def view(cls, view_cls: Type[ViewT]) -> Type[ViewT]:
        cls._view_cls = view_cls
        return view_cls

    def __del__(self) -> None:
        if not self._is_destroyed:
            warnings.warn('Component instance about to be destroyed but destroy() has not been called')


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


_ThisComponent = NewType('_ThisComponent', Component)


class _ComponentContextModule(Module):
    def __init__(self, component: Component) -> None:
        self._component = component

    def configure(self, binder: Binder) -> None:
        binder.bind(
            interface=_ThisComponent,
            to=InstanceProvider(self._component)
        )

        if self._component._presenter_cls is not None:
            binder.bind(
                interface=self._component._presenter_cls,
                to=CallableProvider(lambda: self._component._presenter_obj)
            )


class WidgetComponent(Component):
    @inject
    def __init__(self, parent_injector: Optional[Injector] = None, **kwargs) -> None:
        super().__init__(
            parent_injector=parent_injector,
            **kwargs
        )

        widget = cast(WidgetView, self._view_obj)._widget
        assert widget is not None

        self.widget = widget
        self._destroy_id = widget.connect('destroy', self._hdl_widget_destroy)

    def _hdl_widget_destroy(self, widget: Gtk.Widget) -> None:
        widget.disconnect(self._destroy_id)
        self.destroy()

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
