import os
import unittest
from unittest.mock import patch

from managers.database_manager import DatabaseManager
from managers.player_data_manager import PlayerDataManager
from models.character import Character
from models.character_class import CharacterClass
from models.inventory import Inventory
from models.weapon import Weapon
from prefabs.items import create_item

TEST_DB = "test_game.db"


def make_character(name="Sito"):
    """Returns a character with 2 potions and 2 defeated enemies."""
    inventory = Inventory()
    inventory.add_item(create_item("potion"))
    inventory.add_item(create_item("potion"))
    return Character(name, CharacterClass(), Weapon(), inventory,
                     level=2, xp=10, gold=50, defeated_enemies=["Goblin", "Kobold"])


class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        # use a test database instead of the real game.db
        self.db = DatabaseManager(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_empty_database_returns_none(self):
        self.assertIsNone(self.db.load_character())

    def test_save_and_load_returns_same_data(self):
        data = make_character().to_dict()
        self.db.save_character(data)

        self.assertEqual(self.db.load_character(), data)

    def test_saving_again_keeps_only_the_last_character(self):
        self.db.save_character(make_character("Old").to_dict())
        self.db.save_character(make_character("New").to_dict())

        loaded = self.db.load_character()
        self.assertEqual(loaded["name"], "New")
        self.assertEqual(len(loaded["inventory"]["items"]), 2)

    def test_player_data_manager_saves_and_loads_character(self):
        manager = PlayerDataManager()
        manager._database_manager = self.db
        with patch.object(manager._screen_manager, "message"):
            manager.save_data(make_character())
            loaded = manager.load_data()

        self.assertEqual(loaded.name, "Sito")
        self.assertEqual(loaded.level, 2)
        self.assertEqual(len(loaded.inventory.items), 2)
        self.assertEqual(loaded.defeated_enemies, {"Goblin", "Kobold"})


if __name__ == "__main__":
    unittest.main()
