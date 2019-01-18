import collections
import itertools
from typing import TypeVar, Optional, Sequence, Callable, Mapping, Union, Any

from .bindable import AtomicBindable, Bindable, AtomicBindableVar
from .binding import Binding
from .set import SetBindable, BuiltinSetBindable

BindableType = TypeVar('BindableType', bound=Bindable)
TxT = TypeVar('TxT')
VT = TypeVar('VT')


class BindableProxy(Bindable[TxT]):
    def __init__(self, target: Bindable[TxT]) -> None:
        super().__init__()
        self._proxy_target_value = None  # type: Optional[Bindable[TxT]]
        self._proxy_target_cleanup_tasks = []
        self._proxy_target = target

    def __call__(self, bindable: BindableType) -> BindableType:
        Binding(self, bindable)
        return bindable

    @property
    def _proxy_target(self) -> Bindable[TxT]:
        return self._proxy_target_value

    @_proxy_target.setter
    def _proxy_target(self, new_target: Bindable[TxT]) -> None:
        self._remove_current_proxy_target()
        self._proxy_target_value = new_target
        self._proxy_target_cleanup_tasks.append(
            new_target.on_new_tx.connect(self._bcast_tx).disconnect)
        self._bcast_tx(self._export())

    def _remove_current_proxy_target(self) -> None:
        for f in self._proxy_target_cleanup_tasks:
            f()
        self._proxy_target_cleanup_tasks = []
        self._proxy_target_value = None

    def _export(self) -> TxT:
        return self._proxy_target._export()

    def _raw_apply_tx(self, tx: TxT) -> Optional[Sequence[TxT]]:
        return self._proxy_target._raw_apply_tx(tx)


class IfExpr(BindableProxy[TxT]):
    def __init__(self, cond: AtomicBindable[bool], true: Bindable[TxT], false: Bindable[TxT]) -> None:
        initial_target = true if cond.get() else false
        super().__init__(target=initial_target)

        self._cond = cond
        self._true = true
        self._false = false

        self._cond.on_changed.connect(self._hdl_cond_changed)

    def _hdl_cond_changed(self) -> None:
        new_target = self._true if self._cond.get() else self._false
        self._proxy_target = new_target


if_expr = IfExpr


# AtomicBindableFunction

ArgType = Union[AtomicBindable, SetBindable]


class FunctionApplierBindable(BindableProxy[VT]):
    def __init__(self, func: Callable[..., VT], args: Sequence[ArgType], kwargs: Mapping[str, ArgType]) -> None:
        self._func = func
        self._args = tuple(args)
        self._kwargs = dict(kwargs)
        initial_result = self._calculate_result()

        super().__init__(self._convert_to_bindable(initial_result))

        for x in itertools.chain(self._args, self._kwargs.values()):
            if not isinstance(x, Bindable):
                continue
            x.on_new_tx.connect(self._update, ignore_args=True)

    @staticmethod
    def _convert_to_pod(x: ArgType) -> Any:
        if not isinstance(x, Bindable):
            return x
        bindable = x
        if isinstance(bindable, AtomicBindable):
            return bindable.get()
        elif isinstance(bindable, SetBindable):
            return set(bindable)
        else:
            raise ValueError('Unrecognized bindable type')

    @staticmethod
    def _convert_to_bindable(x: ArgType) -> Any:
        if isinstance(x, collections.Set):
            return BuiltinSetBindable(x)
        else:
            return AtomicBindableVar(x)

    def _calculate_result(self) -> VT:
        args_pod = [self._convert_to_pod(x) for x in self._args]
        kwargs_pod = {k: self._convert_to_pod(v) for k, v in self._kwargs.items()}
        return self._func(*args_pod, **kwargs_pod)

    def _update(self) -> None:
        result = self._calculate_result()
        self._proxy_target = self._convert_to_bindable(result)

    def _raw_apply_tx(self, tx: Any) -> None:
        raise ValueError("Can't apply transactions to this.")


class FunctionBindableWrapper:
    def __init__(self, func: Callable) -> None:
        self._func = func

    def __call__(self, *args, **kwargs) -> Any:
        return FunctionApplierBindable(self._func, args, kwargs)


bindable_function = FunctionBindableWrapper
