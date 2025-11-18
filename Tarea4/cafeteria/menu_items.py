from __future__ import annotations
from abc import ABC, abstractmethod


class MenuItem(ABC):
    """Componente abstracto en el patrón Decorator.

    Representa un ítem que se puede ordenar en la cafetería.
    """

    @abstractmethod
    def description(self) -> str:
        """Devuelve una descripción legible del ítem."""
        raise NotImplementedError

    @abstractmethod
    def cost(self) -> float:
        """Devuelve el costo del ítem."""
        raise NotImplementedError

    @abstractmethod
    def category(self) -> str:
        """Devuelve la categoría: 'bebida' o 'alimento'."""
        raise NotImplementedError


class BasicBeverage(MenuItem):
    """Componente concreto que representa una bebida base."""

    def __init__(self, name: str, price: float) -> None:
        self._name = name
        self._price = price

    def description(self) -> str:
        return self._name

    def cost(self) -> float:
        return self._price

    def category(self) -> str:
        return "bebida"


class BasicFood(MenuItem):
    """Componente concreto que representa un alimento base."""

    def __init__(self, name: str, price: float) -> None:
        self._name = name
        self._price = price

    def description(self) -> str:
        return self._name

    def cost(self) -> float:
        return self._price

    def category(self) -> str:
        return "alimento"
