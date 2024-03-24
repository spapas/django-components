from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Type, TypeVar

if TYPE_CHECKING:
    from django_components import component

_TC = TypeVar("_TC", bound=Type["component.Component"])


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception) :
    pass


class ComponentRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, type[component.Component]] = {}  # component name -> component_class mapping

    def register(self, name: str, component: type[component.Component]) -> None:
        existing_component = self._registry.get(name)
        if existing_component and existing_component.class_hash != component.class_hash:
            raise AlreadyRegistered('The component "%s" has already been registered' % name)
        self._registry[name] = component

    def unregister(self, name: str) -> None:
        self.get(name)

        del self._registry[name]

    def get(self, name: str) -> type[component.Component]:
        if name not in self._registry:
            raise NotRegistered('The component "%s" is not registered' % name)

        return self._registry[name]

    def all(self) -> dict[str, type[component.Component]]:
        return self._registry

    def clear(self) -> None:
        self._registry = {}


# This variable represents the global component registry
registry: ComponentRegistry = ComponentRegistry()


def register(name: str) -> Callable[[_TC], _TC]:
    """Class decorator to register a component.

    Usage:

    @register("my_component")
    class MyComponent(component.Component):
        ...
    """

    def decorator(component: _TC) -> _TC:
        registry.register(name=name, component=component)
        return component

    return decorator
