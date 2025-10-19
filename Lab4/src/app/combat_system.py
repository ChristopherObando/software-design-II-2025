
from src.app.i_combat_system import ICombatSystem

class CombatSystem(ICombatSystem):
    def __init__(self, damage_calculator):
        self.damage_calculator = damage_calculator
    
    def perform_attack(self, attacker, weapon, target):
        if not target.is_alive:
            return f"{target.name} ya está derrotado"
        
        result = weapon.attack(attacker, target)
        critical = self.damage_calculator.check_critical_hit()
        
        if critical:
            bonus_damage = 10
            target.take_damage(bonus_damage)
            result += f" ¡GOLPE CRÍTICO! +{bonus_damage} daño extra"
        
        return result