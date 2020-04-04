from typing import MutableSequence, Tuple, Sequence

import cairo

from opendrop.widgets.composition.abc import Composition


class LayeredComposition(Composition):
    def __init__(self, **properties) -> None:
        super().__init__(**properties)

        self._children = []  # type: MutableSequence[_LayeredCompositionChild]

    def draw(self, cr: cairo.Context) -> None:
        for composition in self._compositions:
            composition.draw(cr)

    def map(self) -> None:
        for composition in self._compositions:
            composition.map()

    def unmap(self) -> None:
        for composition in self._compositions:
            composition.unmap()

    def _do_size_allocate(self, size: Tuple[int, int]) -> None:
        for composition in self._compositions:
            composition.size_allocate(size)

    def add_layer(self, composition: Composition, z_index: int = 0) -> None:
        child = _LayeredCompositionChild(self, composition, z_index)
        self._children.append(child)
        self._arrange_children()
        self.invalidate()

    def remove_layer(self, composition: Composition):
        child = self._find_child_from_composition(composition)
        child.disconnect()
        self._children.remove(child)
        self.invalidate()

    @property
    def _compositions(self) -> Sequence[Composition]:
        return tuple(
            child.composition
            for child in self._children
        )

    def _arrange_children(self) -> None:
        self._children = sorted(self._children, key=lambda child: child.z_index)

    def _find_child_from_composition(self, composition: Composition) -> '_LayeredCompositionChild':
        for child in self._children:
            if child.composition == composition:
                return child
        else:
            raise ValueError

    def _child_invalidate(self, region: cairo.Region) -> None:
        self.invalidate(region)


class _LayeredCompositionChild:
    def __init__(self, parent: LayeredComposition, composition: Composition, z_index: int) -> None:
        self._parent = parent

        self.composition = composition
        self.z_index = z_index

        self._hdl_composition_invalidate_event_id = composition.connect(
            'invalidate-event', self._hdl_composition_invalidate_event
        )

    def _hdl_composition_invalidate_event(self, composition: Composition, region: cairo.Region) -> None:
        self._parent._child_invalidate(region)

    def disconnect(self) -> None:
        self.composition.disconnect(self._hdl_composition_invalidate_event_id)
