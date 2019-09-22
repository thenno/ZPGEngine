from copy import deepcopy
from dataclasses import dataclass
from typing import Tuple, Set
from collections import defaultdict


class Component:
    pass


class AutoClean:
    pass


class Entities:
    def __init__(self, entities):
        self._entities = entities

    def filter(self, component_classes):
        result = None
        for component_class in component_classes:
            entities = {
                entity
                for entity, _ in enumerate(self._entities[component_class])
                if self._entities[component_class][entity] is not None
            }
            result = entities if result is None else result & entities
        yield from result or []

    def get(self, entity, component_class):
        return self._entities[component_class][entity]

    def set(self, entity, component_class, value):
        self._entities[component_class][entity] = value

    @property
    def count(self):
        for entities in self._entities.values():
            return len(entities)


class Components:
    def __init__(self, entities):
        self._entities = entities
        self._components = defaultdict(list)
        for cs, components in entities.items():
            for entity, component in enumerate(components):
                self._components[component].append(entity)

    def get(self, component):
        return self._components[component]

    def get_need_clean(self):
        for component_class in self._entities:
            if issubclass(component_class, AutoClean):
                yield component_class


class Manager:
    def __init__(self, components):
        self.components = Components(components)
        self.entities = Entities(components)
        self._components = components

    def clone(self):
        return Manager(deepcopy(self._components))

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
class Movable(Component):
    pass


@dataclass(frozen=True)
class AI(Component):
    pass


@dataclass(frozen=True)
class Vision(Component):
    pass


@dataclass(frozen=True)
class FOV(Component, AutoClean):
    fov: Set


@dataclass(frozen=True)
class Actions(Component, AutoClean):
    actions: Tuple


@dataclass(frozen=True)
class Viewer:
    pass
