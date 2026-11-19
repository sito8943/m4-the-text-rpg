import unittest
from unittest.mock import patch

from managers.action_manager import ActionManager
from models.character import Character
from models.character_class import CharacterClass
from models.inventory import Inventory
from models.weapon import Weapon
from prefabs.items import create_item


# Character and Inventory print to the console; the fake print keeps the test output clean
@patch("builtins.print")
class TestInventory(unittest.TestCase):

    def setUp(self):
        self.actions = ActionManager()
        # default class: max HP 100
        self.hero = Character("Sito", CharacterClass(), Weapon(), Inventory())
        self.hero.inventory.items = [create_item("potion"), create_item("potion")]
        # the player's answers are given by each test; no real screen is shown
        self.menu = patch.object(self.actions._screen_manager, "print_menu").start()
        self.message = patch.object(self.actions._screen_manager, "message").start()
        self.addCleanup(patch.stopall)

    def test_using_potion_heals_and_removes_it(self, _):
        self.hero.hp = 50
        self.menu.side_effect = ["1", "2"]  # use the first potion, then Back (1 potion left, so Back is 2)

        self.actions._inventory(self.hero)

        self.assertEqual(self.hero.hp, 80)  # Potion restores 30 HP
        self.assertEqual(len(self.hero.inventory.items), 1)

    def test_potion_is_not_used_with_full_hp(self, _):
        self.menu.side_effect = ["1", "3"]

        self.actions._inventory(self.hero)

        self.assertEqual(len(self.hero.inventory.items), 2)

    def test_back_leaves_inventory_without_changes(self, _):
        self.hero.hp = 50
        self.menu.return_value = "3"

        self.actions._inventory(self.hero)

        self.assertEqual(self.hero.hp, 50)
        self.assertEqual(len(self.hero.inventory.items), 2)

    def test_empty_inventory_shows_message(self, _):
        self.hero.inventory.items = []

        self.actions._inventory(self.hero)

        self.menu.assert_not_called()
        self.message.assert_called_once()


if __name__ == "__main__":
    unittest.main()
