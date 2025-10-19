from abc import ABC, abstractmethod

class IDamageCalculator(ABC):
    @abstractmethod
    def check_critical_hit(self):
        pass