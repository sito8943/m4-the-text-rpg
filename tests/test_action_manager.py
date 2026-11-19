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


# Character, Inventory and Wallet print to the console; the fake print keeps the test output clean
@patch("builtins.print")
class TestShop(unittest.TestCase):

    def setUp(self):
        self.actions = ActionManager()
        # starts "Unarmed" (damage 1), so every weapon is on sale:
        # 1 Potion, 2 Sword, 3 Axe, 4 War Hammer, 5 Back
        self.hero = Character("Sito", CharacterClass(), Weapon(), Inventory())
        # the player's answers are given by each test; no real screen is shown
        self.menu = patch.object(self.actions._screen_manager, "print_menu").start()
        self.message = patch.object(self.actions._screen_manager, "message").start()
        self.addCleanup(patch.stopall)

    def test_buy_potion_with_enough_gold(self, _):
        self.hero.wallet.gold = 20
        self.menu.side_effect = ["1", "5"]  # buy a potion, then Back

        self.actions._shop(self.hero)

        self.assertEqual(self.hero.wallet.gold, 5)  # potion costs 15
        self.assertEqual(len(self.hero.inventory.items), 1)

    def test_cannot_buy_without_enough_gold(self, _):
        self.hero.wallet.gold = 10
        self.menu.side_effect = ["1", "5"]

        self.actions._shop(self.hero)

        self.assertEqual(self.hero.wallet.gold, 10)
        self.assertEqual(len(self.hero.inventory.items), 0)

    def test_buy_weapon_equips_it(self, _):
        self.hero.wallet.gold = 50
        # buy the Sword, then Back (Sword is no longer on sale, so Back is 4)
        self.menu.side_effect = ["2", "4"]

        self.actions._shop(self.hero)

        self.assertEqual(self.hero.weapon.name, "Sword")
        self.assertEqual(self.hero.wallet.gold, 10)  # sword costs 40

    def test_only_better_weapons_are_on_sale(self, _):
        self.hero.weapon = Weapon("Axe", 7)
        self.menu.return_value = "3"  # Potion, War Hammer, Back

        self.actions._shop(self.hero)

        labels = self.menu.call_args[0][1]  # second argument given to print_menu
        self.assertEqual(len(labels), 3)
        self.assertIn("War Hammer", labels[1])


if __name__ == "__main__":
    unittest.main()
