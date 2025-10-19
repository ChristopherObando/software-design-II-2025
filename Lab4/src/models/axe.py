from src.models.weapon import Weapon

class Axe(Weapon):
    def attack(self, attacker, target):
        damage = 20
        target.take_damage(damage)
        return f"{attacker.name} ataca con hacha a {target.name} causando {damage} de daño"
