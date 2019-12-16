import asyncio
from typing import Type, Optional, Callable

from injector import inject, Binder, InstanceProvider

from opendrop.utility.program import Program
from .component import Component
from .component_factory import _ComponentFactoryModule, ComponentFactory
from .event_loop import _EventLoopModule
from .window_context import _WindowContextModule


class Bootstrap(Program):
    modules = [_EventLoopModule, _ComponentFactoryModule, _WindowContextModule]

    def __init__(self, entry: Type[Component]) -> None:
        super().__init__()

        self._entry = entry

        self._root_component = None  # type: Optional[Component]

        self._stop_flag = None  # type: Optional[asyncio.Event]

    def configure(self, binder: Binder) -> None:
        quit_service = QuitService(do_quit=self.stop)
        binder.bind(interface=QuitService, to=InstanceProvider(quit_service))

    @inject
    def main(self, cf: ComponentFactory, loop: asyncio.AbstractEventLoop) -> None:
        self._stop_flag = asyncio.Event(loop=loop)

        self._root_component = cf.create(self._entry)

        loop.run_until_complete(self._stop_flag.wait())

        self._root_component.destroy()

    def stop(self) -> None:
        if self._stop_flag is None:
            return

        self._stop_flag.set()


class QuitService:
    def __init__(self, do_quit: Callable) -> None:
        self._do_quit = do_quit

    def quit(self) -> None:
        self._do_quit()
