from abc import ABC, abstractmethod

class Weapon(ABC):
    @abstractmethod
    def attack(self, attacker, target):
        pass