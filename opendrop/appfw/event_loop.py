import asyncio

from injector import Module, Binder, InstanceProvider


class _EventLoopModule(Module):
    def configure(self, binder: Binder) -> None:
        from opendrop.vendor.glibcoro import GLibEventLoopPolicy
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())

        binder.bind(
            interface=asyncio.AbstractEventLoop,
            to=InstanceProvider(asyncio.get_event_loop()),
        )
