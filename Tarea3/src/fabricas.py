
"""
fabricas.py
Implementación del patrón Factory Method para crear pedidos concretos.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from src.pedidos import Pedido, PedidoHamburguesa, PedidoPizza

class CreadorPedidos(ABC):
    """Interfaz del creador: define el Factory Method `crear_pedido`."""

    @abstractmethod
    def crear_pedido(self, id_pedido: int) -> Pedido:
        """Crea un Pedido concreto."""
        raise NotImplementedError


class CreadorHamburguesas(CreadorPedidos):
    def crear_pedido(self, id_pedido: int) -> Pedido:
        return PedidoHamburguesa(id_pedido=id_pedido)


class CreadorPizzas(CreadorPedidos):
    def crear_pedido(self, id_pedido: int) -> Pedido:
        return PedidoPizza(id_pedido=id_pedido)
