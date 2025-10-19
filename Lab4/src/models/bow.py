from src.models.weapon import Weapon

class Bow(Weapon):
    def attack(self, attacker, target):
        damage = 12
        target.take_damage(damage)
        return f"{attacker.name} dispara flecha a {target.name} causando {damage} de daño"