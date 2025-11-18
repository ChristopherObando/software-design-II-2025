from __future__ import annotations
from dataclasses import dataclass
from typing import List
from customers import Customer
from menu_items import MenuItem
from observer import Subject


@dataclass
class Order:
    """Representa un pedido de un MenuItem hecho por un cliente."""
    customer: Customer
    item: MenuItem


class OrderManager(Subject):
    """Mantiene la lista de pedidos y actúa como Subject en el patrón Observer."""

    def __init__(self) -> None:
        super().__init__()
        self._orders: List[Order] = []

    def add_order(self, order: Order) -> None:
        self._orders.append(order)

    @property
    def pending_orders(self) -> List[Order]:
        """Devuelve una copia de la lista de pedidos pendientes."""
        return list(self._orders)
