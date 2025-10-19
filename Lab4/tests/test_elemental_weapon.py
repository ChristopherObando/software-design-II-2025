# tests/test_elemental_weapon.py
import unittest
from unittest.mock import MagicMock
from src.app.combat_system import CombatSystem
from src.models.character import Character
from src.models.sword import Sword
from src.models.imbued_weapon import ImbuedWeapon
from src.models.elements import Element

class TestElementalWeapon(unittest.TestCase):

    def test_elemental_basic_bonus_no_crit(self):
        calc = MagicMock()
        # Aunque devolviera True, el arma imbuida debe desactivar el crítico.
        calc.check_critical_hit.return_value = True

        combat = CombatSystem(calc)
        hero = Character("Hero")
        enemy = Character("Enemy")

        weapon = ImbuedWeapon(Sword(), Element.FIRE)
        msg = combat.perform_attack(hero, weapon, enemy)

        # Sword: 15 base + 5 elemental = 20 total
        self.assertEqual(enemy.health, 80)
        self.assertIn("Daño elemental (+5)", msg)
        # El crítico NO se consulta ni aplica
        calc.check_critical_hit.assert_not_called()
        # Elemento pegado
        self.assertIn(Element.FIRE, enemy.elements)

    def test_elemental_reaction_triple_bonus_and_clears(self):
        calc = MagicMock()
        calc.check_critical_hit.return_value = True  # no debería llamarse

        combat = CombatSystem(calc)
        hero = Character("Hero")
        enemy = Character("Enemy")

        fire_sword = ImbuedWeapon(Sword(), Element.FIRE)
        water_sword = ImbuedWeapon(Sword(), Element.WATER)

        # Primer golpe: FUEGO (15 + 5) => 80, pega FUEGO
        combat.perform_attack(hero, fire_sword, enemy)
        self.assertEqual(enemy.health, 80)
        self.assertIn(Element.FIRE, enemy.elements)

        # Segundo golpe: AGUA produce reacción => (15 + 15) => 50
        msg = combat.perform_attack(hero, water_sword, enemy)
        self.assertEqual(enemy.health, 50)
        self.assertIn("REACCIÓN ELEMENTAL", msg)
        # Tras reacción, elementos limpiados
        self.assertEqual(len(enemy.elements), 0)

        # Tercer golpe: AGUA de nuevo, SIN reacción => (15 + 5) => 30
        combat.perform_attack(hero, water_sword, enemy)
        self.assertEqual(enemy.health, 30)
        self.assertIn(Element.WATER, enemy.elements)

        # Crítico nunca consultado en arma imbuida
        calc.check_critical_hit.assert_not_called()
