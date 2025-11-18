from __future__ import annotations
from abc import ABC
from menu_items import MenuItem


class ExtraDecorator(MenuItem, ABC):
    """Decorador base que envuelve un MenuItem y delega comportamiento."""

    def __init__(self, base_item: MenuItem) -> None:
        self._base_item = base_item

    def cost(self) -> float:
        # Por simplicidad, cada extra suma un pequeño costo extra.
        return self._base_item.cost() + 200.0

    def category(self) -> str:
        # El extra no cambia la categoría del ítem.
        return self._base_item.category()


class Milk(ExtraDecorator):
    """Agrega leche a una bebida."""

    def description(self) -> str:
        base = self._base_item.description()
        if "con" in base.lower():
            return f"{base} y leche"
        return f"{base} con leche"


class Cinnamon(ExtraDecorator):
    """Agrega canela a una bebida."""

    def description(self) -> str:
        base = self._base_item.description()
        if "con" in base.lower():
            return f"{base} y canela"
        return f"{base} con canela"


class Cream(ExtraDecorator):
    """Agrega crema a una bebida."""

    def description(self) -> str:
        base = self._base_item.description()
        if "con" in base.lower():
            return f"{base} y crema"
        return f"{base} con crema"


class ChocolateFilling(ExtraDecorator):
    """Agrega relleno de chocolate a un alimento (ej. croissant)."""

    def description(self) -> str:
        base = self._base_item.description()
        if "con" in base.lower():
            return f"{base} y relleno de chocolate"
        return f"{base} con relleno de chocolate"
