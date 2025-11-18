from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    """Interface que cualquier observador debe implementar."""

    @abstractmethod
    def update(self, message: str) -> None:
        """Reacciona a un mensaje enviado por el Subject."""
        raise NotImplementedError


class Subject:
    """Subject en el patrón Observer. Maneja una lista de observadores."""

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, message: str) -> None:
        for observer in self._observers:
            observer.update(message)


class NotificationService(Observer):
    """Observador concreto que imprime notificaciones del sistema."""

    def update(self, message: str) -> None:
        print(f"[Sistema]: {message}")
