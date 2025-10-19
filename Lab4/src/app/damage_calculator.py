import random
from src.app.i_damage_calculator import IDamageCalculator

class StandardDamageCalculator(IDamageCalculator):
    def check_critical_hit(self):
        return random.random() < 0.2  # 20% de probabilidad