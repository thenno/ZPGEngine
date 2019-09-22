from copy import deepcopy
from dataclasses import dataclass
from typing import List


class Component:
    pass


class AutoClean:
    pass


class ComponentManager:
    def __init__(self, components):
        self._components = components

    def filter(self, component_classes):
        result = None
        for component_class in component_classes:
            entities = {
                entity
                for entity, _ in enumerate(self._components[component_class])
                if self._components[component_class][entity] is not None
            }
            result = entities if result is None else result & entities
        if result is not None:
            yield from result

    def get(self, entity, component_class):
        return self._components[component_class][entity]

    def get_need_clean(self):
        for component_class in self._components:
            if issubclass(component_class, AutoClean):
                yield component_class

    @property
    def entities_count(self):
        for entities in self._components.values():
            return len(entities)

    def set(self, entity, component_class, value):
        self._components[component_class][entity] = value

    def clone(self):
        return ComponentManager(deepcopy(self._components))

    def serialize(self):
        return self._components


@dataclass(frozen=True)
class Position(Component):
    x: int
    y: int


@dataclass(frozen=True)
class Visible(Component):
    char: str


@dataclass(frozen=True)
class Name(Component):
    name: str


@dataclass(frozen=True)
class NextPosition(Component, AutoClean):
    x: int
    y: int


@dataclass(frozen=True)
class PermittedPositions(Component, AutoClean):
    positions: List[Position]


class Movable(Component, AutoClean):
    pass
