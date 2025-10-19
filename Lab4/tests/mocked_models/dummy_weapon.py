from src.models.weapon import Weapon

class DummyWeapon(Weapon):
    """Arma dummy para testing que no hace daño real"""
    def attack(self, attacker, target):
        return f"{attacker.name} usa arma dummy en {target.name}"