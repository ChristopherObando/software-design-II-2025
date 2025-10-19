import unittest
from unittest.mock import MagicMock
from src.app.combat_system import CombatSystem
from src.models.character import Character
from src.models.sword import Sword

class TestCombatSystemEdges(unittest.TestCase):

    def test_no_attack_when_target_is_dead(self):
        calc = MagicMock()
        calc.check_critical_hit.return_value = True  # no debería ni llamarse

        combat = CombatSystem(calc)
        hero = Character("Hero")
        enemy = Character("Enemy")
        enemy.take_damage(100)  # dejarlo muerto

        msg = combat.perform_attack(hero, Sword(), enemy)

        self.assertEqual(msg, f"{enemy.name} ya está derrotado")
        calc.check_critical_hit.assert_not_called()
