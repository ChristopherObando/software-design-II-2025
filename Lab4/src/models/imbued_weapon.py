# src/models/imbued_weapon.py
from src.models.weapon import Weapon
from src.models.elements import Element

class ImbuedWeapon(Weapon):
    """
    Decorador de arma que agrega daño elemental y gestiona reacciones.
    Reglas:
      - Daño elemental base: +5.
      - Si el objetivo ya tiene un elemento DISTINTO => REACCIÓN => +15 (triple del bono).
      - Las armas imbuidas DESACTIVAN el crítico.
      - Tras reacción, se limpian los elementos del objetivo (no se aplica el nuevo).
      - Si NO hay reacción, el elemento del arma queda aplicado al objetivo.
    """
    disable_critical = True  # bandera para que el CombatSystem omita el crítico

    def __init__(self, base_weapon: Weapon, element: Element):
        self.base_weapon = base_weapon
        self.element = element

    def attack(self, attacker, target):
        # 1) daño base del arma envuelta
        base_msg = self.base_weapon.attack(attacker, target)

        # 2) determinar si hay reacción
        bonus = 5
        reaction = False
        target_elements = getattr(target, "elements", set())

        if target_elements and self.element not in target_elements:
            # reacción elemental
            reaction = True
            bonus = 15
            # limpiar elementos al objetivo (regla explicitada)
            target.clear_elements()

        # 3) aplicar daño elemental
        target.take_damage(bonus)

        # 4) si NO hubo reacción, aplicamos/pegamos el elemento actual
        if not reaction:
            target.apply_element(self.element)

        # 5) mensaje
        if reaction:
            return f"{base_msg}. ¡REACCIÓN ELEMENTAL! +{bonus} de daño"
        return f"{base_msg}. Daño elemental (+{bonus}) [{self.element.name.lower()}]"
