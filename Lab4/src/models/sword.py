from src.models.weapon import Weapon

class Sword(Weapon):
    def attack(self, attacker, target):
        damage = 15
        target.take_damage(damage)
        return f"{attacker.name} ataca con espada a {target.name} causando {damage} de daño"
