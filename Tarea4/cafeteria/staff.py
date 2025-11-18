from __future__ import annotations
from orders import Order


class Barista:
    """Responsable de preparar bebidas."""

    def prepare(self, order: Order) -> None:
        print(f"[Barista]: Preparo bebida: {order.item.description()}")


class PastryChef:
    """Responsable de preparar alimentos."""

    def prepare(self, order: Order) -> None:
        print(f"[Pastelero]: Preparo alimento: {order.item.description()}")
