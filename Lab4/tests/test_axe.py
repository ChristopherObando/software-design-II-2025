import unittest
from unittest.mock import MagicMock
from src.app.combat_system import CombatSystem
from src.models.character import Character
from src.models.axe import Axe

class TestAxe(unittest.TestCase):

    def test_axe_base_damage_without_critical(self):
        calc = MagicMock()
        calc.check_critical_hit.return_value = False

        combat = CombatSystem(calc)
        hero = Character("Hero")
        enemy = Character("Enemy")
        axe = Axe()

        msg = combat.perform_attack(hero, axe, enemy)

        self.assertEqual(enemy.health, 80)          # 100 - 20
        self.assertIn("hacha", msg)
        self.assertIn("20", msg)
        calc.check_critical_hit.assert_called_once()

    def test_axe_with_critical_adds_bonus(self):
        calc = MagicMock()
        calc.check_critical_hit.return_value = True

        combat = CombatSystem(calc)
        hero = Character("Hero")
        enemy = Character("Enemy")
        axe = Axe()

        msg = combat.perform_attack(hero, axe, enemy)

        self.assertEqual(enemy.health, 70)          # 100 - (20 + 10)
        self.assertIn("GOLPE CRÍTICO", msg)
        calc.check_critical_hit.assert_called_once()
