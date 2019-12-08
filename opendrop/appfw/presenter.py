from typing import Generic, TypeVar

ViewT = TypeVar('ViewT')


class Presenter(Generic[ViewT]):
    def after_view_init(self, view: ViewT) -> None:
        pass

    def before_view_destroy(self) -> None:
        pass

    def destroy(self) -> None:
        pass
