
"""
pedidos.py
Dominio de la aplicación: definición de los Pedidos (abstracto y concretos).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import time
import random

class Pedido(ABC):
    """Representa un pedido genérico a preparar por un cocinero."""
    def __init__(self, id_pedido: int) -> None:
        self.id_pedido = id_pedido

    @property
    @abstractmethod
    def tipo(self) -> str:
        """Nombre del tipo de pedido (p.ej., 'Hamburguesa' o 'Pizza')."""
        raise NotImplementedError

    @abstractmethod
    def preparar(self) -> str:
        """
        Simula la preparación del pedido y devuelve un mensaje de resultado.
        Cada tipo puede variar el tiempo o pasos.
        """
        raise NotImplementedError


class PedidoHamburguesa(Pedido):
    @property
    def tipo(self) -> str:
        return "Hamburguesa"

    def preparar(self) -> str:
        # Simulación del tiempo de preparación
        time.sleep(random.uniform(0.3, 0.9))
        return f"Hamburguesa {self.id_pedido} preparada"


class PedidoPizza(Pedido):
    @property
    def tipo(self) -> str:
        return "Pizza"

    def preparar(self) -> str:
        # Simulación del tiempo de preparación (ligeramente distinto)
        time.sleep(random.uniform(0.4, 1.2))
        return f"Pizza {self.id_pedido} preparada"
