import asyncio

from injector import Module, Binder, InstanceProvider


class _EventLoopModule(Module):
    def configure(self, binder: Binder) -> None:
        from opendrop.vendor.glibcoro import glibcoro
        glibcoro.install()

        binder.bind(
            interface=asyncio.AbstractEventLoop,
            to=InstanceProvider(asyncio.get_event_loop()),
        )
