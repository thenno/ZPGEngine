from copy import deepcopy
from dataclasses import dataclass
from typing import Tuple, FrozenSet, Dict, Optional, Type, List
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
    def __init__(self, components: Optional[Dict[Type, List[Optional[Component]]]] = None):
        if components is None:
            components = defaultdict(list)
        self.components = Components(components)
        self.entities = Entities(components)
        self._components = components
        self._components_classes = list(components.keys())

    def clone(self):
        return Manager(deepcopy(self._components))

    def serialize(self):
        return self._components

    def add(self, entity: 'EntityBuilder'):
        components = deepcopy(self._components)
        for cls, component in entity.to_dict().items():
            components[cls].append(component)
        return Manager(components)


@dataclass(frozen=True)
class Position(Component):
    x: int
    y: int


@dataclass(frozen=True)
class PositionX(Component):
    coord: int


@dataclass(frozen=True)
class PositionY(Component):
    coord: int


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
    fov: FrozenSet[Position] = frozenset()


@dataclass(frozen=True)
class Actions(Component, AutoClean):
    actions: Tuple = tuple()


@dataclass(frozen=True)
class Viewer(Component):
    pass


@dataclass(frozen=True)
class UnderUserControl(Component):
    pass


@dataclass(frozen=True)
class EntityBuilder:
    name: Name
    actions: Actions = Actions()
    fov: FOV = FOV()
    visible: Optional[Visible] = None
    ai: Optional[AI] = None
    under_user_control: Optional[UnderUserControl] = None
    vision: Optional[Vision] = None
    viewer: Optional[Viewer] = None
    position: Optional[Position] = None
    movable: Optional[Movable] = None

    def to_dict(self) -> Dict[Type, Optional[Component]]:
        return {
            Name: self.name,
            Actions: self.actions,
            FOV: self.fov,
            Visible: self.visible,
            AI: self.ai,
            UnderUserControl: self.under_user_control,
            Vision: self.vision,
            Viewer: self.viewer,
            Position: self.position,
            Movable: self.movable,
        }
