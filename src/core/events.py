from dataclasses import dataclass
from typing import Type

from core.constants import BOARD_SIZE
from core.components import (
    Manager,
    Position,
    Component,
    Actions,
    FOV,
)


@dataclass(frozen=True)
class Event:
    entity: int
    component_class: Type[Component]

    def __call__(self, prev_state: Component):
        pass


@dataclass(frozen=True)
class Move(Event):
    dx: int
    dy: int
    manager: Manager

    def _is_valid(self, position):
        if not (0 <= position.x < BOARD_SIZE and 0 <= position.y < BOARD_SIZE):
            return False
        if self.manager.components.get(position):
            return False
        return True

    def __call__(self, position):
        x = position.x + self.dx
        y = position.y + self.dy
        new_position = Position(x, y)
        if self._is_valid(new_position):
            return new_position
        return position


@dataclass(frozen=True)
class SetActions(Event):
    event: Event

    def __call__(self, actions):
        return Actions(actions.actions + (self.event,))


@dataclass(frozen=True)
class SetFOV(Event):
    fov: FOV

    def __call__(self, fov):
        return FOV(fov.fov | self.fov)


@dataclass(frozen=True)
class Clean(Event):

    def __call__(self, _):
        return self.component_class()
