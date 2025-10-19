import unittest
from src.models.character import Character

class TestCharacter(unittest.TestCase):

    def test_character_starts_alive_with_full_health(self):
        """Test que un personaje nuevo tiene salud completa y está vivo"""
        warrior = Character("Conan")
        self.assertEqual(warrior.health, 100)
        self.assertTrue(warrior.is_alive)

    def test_take_damage_reduces_health_and_can_kill(self):
        """Test que el daño reduce salud y puede matar al personaje"""
        mage = Character("Gandalf")
        mage.take_damage(30)
        self.assertEqual(mage.health, 70)
        
        mage.take_damage(70)
        self.assertFalse(mage.is_alive)